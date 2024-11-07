'use client'

import { useState, useEffect, useRef } from 'react'
import { UserPanel } from './_components/user-panel'
import { ChatMessages } from './_components/chat-messages'
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { useAuth } from '@/hooks/useAuth'
import Cookies from 'js-cookie';
import api from '@/lib/axios';
import { ICompanyRead } from '@/types/company'
import { IUserRead } from '@/types/user'
import { Spinner } from '@/components/Spinner'

export interface ChatMessage {
  user_id: string;
  name: string;
  message: string;
  timestamp: string;
}

export default function Page() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [inputMessage, setInputMessage] = useState('')
  const [users, setUsers] = useState<IUserRead[]>([])
  const { user: currentUser, isLoading } = useAuth()
  const [company, setCompany] = useState<ICompanyRead>()
  const [user, setUser] = useState<IUserRead>()
  const accessToken = Cookies.get("access_token")
  const [isConnectedSend, setIsConnectedSend] = useState(false)
  const [isConnectedHistory, setIsConnectedHistory] = useState(false)
  const [errorSend, setErrorSend] = useState<string | null>(null)
  const [errorHistory, setErrorHistory] = useState<string | null>(null)

  const wsSendRef = useRef<WebSocket | null>(null)
  const wsHistoryRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    const getCompanyByUser = async () => {
      if (currentUser && currentUser.id) {
        try {
          const response = await api.get<IUserRead>(`/users/${currentUser.id}`)
          setUser(response.data)
          if (response.data.administered_company) {
            setCompany(response.data.administered_company)
            return
          }

          if (response.data.company) {
            setCompany(response.data.company)
            return
          }
        } catch (error) {
          console.error('Error fetching user data:', error)
        }
      }
    }

    getCompanyByUser()
  }, [currentUser])

  useEffect(() => {
    if (!accessToken) {
      setErrorHistory('Authentication token missing.')
      return
    }

    const wsHistoryUrl = process.env.NEXT_PUBLIC_WS_HISTORY_URL + accessToken || `ws://localhost:8000/chat/ws/history?token=${accessToken}`
    const wsHistory = new WebSocket(wsHistoryUrl)
    wsHistoryRef.current = wsHistory

    wsHistory.onopen = () => {
      setIsConnectedHistory(true)
      setErrorHistory(null)
    }

    wsHistory.onmessage = (event) => {
      try {
        const message: ChatMessage = JSON.parse(event.data)
        setMessages((prevMessages) => [...prevMessages, message])
      } catch (error) {
        console.error('Error parsing history message:', error)
      }
    }

    wsHistory.onclose = (event) => {
      setIsConnectedHistory(false)
      if (event.code !== 1000) {
        setErrorHistory('History WebSocket connection closed unexpectedly.')
      }
    }

    wsHistory.onerror = () => {
      setErrorHistory('History WebSocket encountered an error.')
      wsHistory.close()
    }

    return () => {
      wsHistory.close()
    }
  }, [accessToken])

  useEffect(() => {
    if (!accessToken) {
      setErrorSend('Authentication token missing.')
      return
    }

    let reconnectTimer: NodeJS.Timeout | null = null

    const connectWebSocketSend = () => {
      const wsSendUrl = process.env.NEXT_PUBLIC_WS_SEND_URL + accessToken || `ws://localhost:8000/chat/ws/send?token=${accessToken}`
      const wsSend = new WebSocket(wsSendUrl)
      wsSendRef.current = wsSend

      wsSend.onopen = () => {
        setIsConnectedSend(true)
        setErrorSend(null)
      }

      wsSend.onmessage = (event) => {
        try {
          const message: ChatMessage = JSON.parse(event.data)
        } catch (error) {
          console.error('Error parsing new message:', error)
        }
      }

      wsSend.onclose = (event) => {
        setIsConnectedSend(false)
        if (event.code !== 1000) {
          setErrorSend('Send WebSocket connection closed unexpectedly.')
          if (!reconnectTimer) {
            reconnectTimer = setTimeout(() => {
              connectWebSocketSend()
              reconnectTimer = null
            }, 5000)
          }
        }
      }

      wsSend.onerror = () => {
        setErrorSend('Send WebSocket encountered an error.')
        wsSend.close()
      }
    }

    connectWebSocketSend()

    return () => {
      if (reconnectTimer) {
        clearTimeout(reconnectTimer)
      }
      wsSendRef.current?.close()
    }
  }, [accessToken])

  useEffect(() => {
    const fetchData = async () => {
      if (user?.administered_company) {
        try {
          const response = await api.get<IUserRead[]>(`/users/company/${user.administered_company.id}`)
          setUsers(response.data)
        } catch (error) {
          console.error('Error fetching users:', error)
        }
      }

      if (user?.company_id && !user.administered_company) {
        try {
          const response = await api.get<IUserRead[]>(`/users/company/${user.company_id}`)
          setUsers(response.data)
        } catch (error) {
          console.error('Error fetching users:', error)
        }
      }
    }

    fetchData()
  }, [user])

  const handleSendMessage = () => {
    if (inputMessage.trim() && wsSendRef.current && wsSendRef.current.readyState === WebSocket.OPEN) {
      wsSendRef.current.send(inputMessage.trim())
      setInputMessage('')
    } else {
      setErrorSend('Unable to send message. Send WebSocket is closed.')
    }
  }

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-gray-100">
        <Spinner className="h-8 w-8" />
      </div>
    )
  }

  if (!user) {
    return (
      <div className="flex h-screen items-center justify-center bg-gray-100">
        <p className="text-lg font-semibold">Please log in to access the chat.</p>
      </div>
    )
  }

  return (
    <div className="flex h-full bg-gray-100">
      <UserPanel users={users} companyName={company?.name || 'Company'} />
      <div className="flex-1 flex flex-col">
        <div className="bg-white shadow-md p-4">
          <h1 className="text-2xl font-bold">{company?.name || 'Chat'} Chat</h1>
          <div className="text-sm text-gray-500">
            {isConnectedSend && isConnectedHistory ? 'Connected' : 'Disconnected'}
          </div>
          {errorSend && (
            <div className="mt-2 text-red-500">
              {errorSend}
            </div>
          )}
          {errorHistory && (
            <div className="mt-2 text-red-500">
              {errorHistory}
            </div>
          )}
        </div>
        <ChatMessages messages={messages} currentUserId={user?.id!} />
        <div className="bg-white p-4 flex space-x-2">
          <Input
            type="text"
            placeholder="Type a message..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
            className="flex-1"
            disabled={!isConnectedSend}
          />
          <Button onClick={handleSendMessage} disabled={!isConnectedSend}>Send</Button>
        </div>
      </div>
    </div>
  )
}
