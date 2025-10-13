import { useEffect, useRef, useState } from 'react'
import './ChatWidget.css'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function ChatWidget() {
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState([
    { text: 'Hi there! 👋 Welcome to Flipkart!', role: 'ai', time: Date.now() },
    { text: 'How can I help you with your shopping today?', role: 'ai', time: Date.now() },
  ])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef(null)
  const textareaRef = useRef(null)

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Apply chat-open class to root
  useEffect(() => {
    const root = document.getElementById('app-root')
    if (!root) return
    
    if (open) {
      root.classList.add('chat-open')
    } else {
      root.classList.remove('chat-open')
    }
    
    return () => {
      root.classList.remove('chat-open')
    }
  }, [open])

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px'
    }
  }, [input])

  const sendMessage = async () => {
    if (!input.trim()) return

    const userMessage = { text: input.trim(), role: 'user', time: Date.now() }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsTyping(true)

    try {
      console.log('� Sending to API:', input.trim())
      
      const response = await fetch(`${API_BASE}/api/chat/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ message: input.trim() }),
      })

      console.log('📡 Response status:', response.status)

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      console.log('✅ API response:', data)

      const aiMessage = { 
        text: data.reply || 'No response from server', 
        role: 'ai', 
        time: Date.now() 
      }
      setMessages(prev => [...prev, aiMessage])

    } catch (error) {
      console.error('❌ Error calling API:', error)
      const errorMessage = { 
        text: 'Sorry, I could not connect to the server. Please try again.', 
        role: 'ai', 
        time: Date.now(),
        error: true
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsTyping(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  if (!open) {
    return (
      <button onClick={() => setOpen(true)} className="chat-open-btn">
        💬 Chat
      </button>
    )
  }

  return (
    <div className="chat-widget-container">
      {/* Header */}
      <div className="chat-header-custom">
        <div className="header-left">
          <div className="header-avatar">🛍️</div>
          <div className="header-title">Flipkart Shop Assistant</div>
        </div>
        <button onClick={() => setOpen(false)} className="chat-close-btn">
          ✕
        </button>
      </div>

      {/* Messages Container */}
      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message-wrapper ${msg.role}`}>
            <div className="message-avatar">
              {msg.role === 'ai' ? '🤖' : '👤'}
            </div>
            <div className="message-content">
              <div className={`message-bubble ${msg.role} ${msg.error ? 'error' : ''}`}>
                {msg.text}
              </div>
              <div className="message-time">
                {new Date(msg.time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="message-wrapper ai">
            <div className="message-avatar">🤖</div>
            <div className="message-content">
              <div className="message-bubble ai typing">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="chat-input-area">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message..."
          className="chat-input-field"
          rows={1}
          disabled={isTyping}
        />
        <button 
          onClick={sendMessage} 
          className="chat-send-btn"
          disabled={!input.trim() || isTyping}
        >
          {isTyping ? '⏳' : '📤'}
        </button>
      </div>
    </div>
  )
}