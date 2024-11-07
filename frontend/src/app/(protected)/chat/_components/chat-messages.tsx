import React, { useEffect, useRef } from 'react'
import { ChatMessage } from '../page'

interface ChatMessagesProps {
  messages: ChatMessage[]
  currentUserId: string
}

export const ChatMessages: React.FC<ChatMessagesProps> = ({ messages, currentUserId }) => {
  const messagesEndRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  return (
    <div className="flex-1 p-4 overflow-y-auto">
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`mb-2 flex ${msg.user_id === currentUserId ? 'justify-end' : 'justify-start'}`}
        >
          <div className={`max-w-xs px-4 py-2 rounded-lg ${msg.user_id === currentUserId ? 'bg-blue-500 text-white' : 'bg-gray-300 text-gray-800'}`}>
            <div className="text-sm font-semibold">{msg.name}</div>
            <div>{msg.message}</div>
            <div className="text-xs text-right">{new Date(msg.timestamp).toLocaleTimeString()}</div>
          </div>
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  )
}
