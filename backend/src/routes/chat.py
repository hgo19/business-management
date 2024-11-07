import os
import json
import asyncio
import uuid
import datetime
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status, HTTPException
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
from dotenv import load_dotenv

from src.models.user import UserResponse
from src.utils.jwt import decode_token
from src.database.connection import get_db
from src.utils.auth import get_current_user

load_dotenv()

chat_router = APIRouter(prefix="/chat", tags=["Chat"])

KAFKA_URL = os.getenv("KAFKA_URL", "localhost:9092")


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.consumer: AIOKafkaConsumer = None
        self.producer: AIOKafkaProducer = None
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        async with self.lock:
            self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        async with self.lock:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        async with self.lock:
            for connection in self.active_connections:
                try:
                    await connection.send_text(message)
                except Exception:
                    pass

    async def start_producer(self):
        if not self.producer:
            self.producer = AIOKafkaProducer(bootstrap_servers=KAFKA_URL)
            await self.producer.start()

    async def start_consumer(self, topic: str):
        if not self.consumer:
            self.consumer = AIOKafkaConsumer(
                topic,
                bootstrap_servers=KAFKA_URL,
                group_id=f"chat_group_{uuid.uuid4()}",
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                value_deserializer=lambda m: m.decode('utf-8'),
            )
            await self.consumer.start()
            asyncio.create_task(self.consume_messages())

    async def consume_messages(self):
        async for msg in self.consumer:
            message = msg.value
            await self.broadcast(message)

    async def shutdown(self):
        async with self.lock:
            if self.consumer:
                await self.consumer.stop()
            if self.producer:
                await self.producer.stop()
            self.active_connections.clear()


manager = ConnectionManager()


async def create_topic_if_not_exists(topic_name: str, bootstrap_servers: str):
    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers, client_id='admin_client')
    try:
        existing_topics = admin_client.list_topics()
        if topic_name not in existing_topics:
            topic = NewTopic(name=topic_name, num_partitions=1, replication_factor=1)
            admin_client.create_topics(new_topics=[topic], validate_only=False)
    finally:
        admin_client.close()


@chat_router.websocket("/ws/history")
async def websocket_history(websocket: WebSocket):
    await websocket.accept()
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        token_data = decode_token(token, credentials_exception)

        get_db_gen = get_db()
        session = await get_db_gen.__anext__()

        try:
            current_user: UserResponse = await get_current_user(token_data, session)
        finally:
            await get_db_gen.aclose()
    except HTTPException:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    company_id = current_user.company_id or (current_user.administered_company.id if current_user.administered_company else None)
    if not company_id:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    topic = f"chat_company_{company_id}"

    await create_topic_if_not_exists(topic, KAFKA_URL)

    temp_consumer_group = f"temp_history_group_{uuid.uuid4()}"
    temp_consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_URL,
        group_id=temp_consumer_group,
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        value_deserializer=lambda m: m.decode('utf-8'),
    )
    await temp_consumer.start()

    try:
        async for msg in temp_consumer:
            message = msg.value
            await websocket.send_text(message)
    finally:
        await temp_consumer.stop()
        await websocket.close()


@chat_router.websocket("/ws/send")
async def websocket_send(websocket: WebSocket):
    await manager.connect(websocket)

    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        token_data = decode_token(token, credentials_exception)

        get_db_gen = get_db()
        session = await get_db_gen.__anext__()

        try:
            current_user: UserResponse = await get_current_user(token_data, session)
        finally:
            await get_db_gen.aclose()
    except HTTPException:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        await manager.disconnect(websocket)
        return

    company_id = current_user.company_id or (current_user.administered_company.id if current_user.administered_company else None)
    if not company_id:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        await manager.disconnect(websocket)
        return
    topic = f"chat_company_{company_id}"

    await create_topic_if_not_exists(topic, KAFKA_URL)

    try:
        await manager.start_producer()
        await manager.start_consumer(topic)
    except Exception:
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        await manager.disconnect(websocket)
        return

    try:
        while True:
            try:
                data = await websocket.receive_text()

                message = {
                    "user_id": current_user.id,
                    "name": current_user.name,
                    "message": data,
                    "timestamp": datetime.datetime.utcnow().isoformat()
                }

                await manager.producer.send_and_wait(topic, json.dumps(message).encode("utf-8"))

            except WebSocketDisconnect:
                await manager.disconnect(websocket)
                break
            except Exception:
                await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
                await manager.disconnect(websocket)
                break
    finally:
        pass


@chat_router.on_event("shutdown")
async def shutdown_event():
    await manager.shutdown()


@chat_router.get("/")
async def get():
    return {"message": "FastAPI Chat Server is running"}
