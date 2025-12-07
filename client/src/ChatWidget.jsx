import { useEffect, useRef, useState, createContext, useContext } from 'react'
import './ChatWidget.css'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

// Auth Context
const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(localStorage.getItem('auth_token'))

  useEffect(() => {
    if (token) {
      localStorage.setItem('auth_token', token)
    } else {
      localStorage.removeItem('auth_token')
    }
  }, [token])

  const login = (newToken, userData) => {
    setToken(newToken)
    setUser(userData)
  }

  const logout = () => {
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}

// Message formatter component
function MessageFormatter({ text }) {
  const formatText = (text) => {
    const parts = text.split(/(\*\*.*?\*\*|\n)/g)
    return parts.map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={i}>{part.slice(2, -2)}</strong>
      } else if (part === '\n') {
        return <br key={i} />
      }
      return part
    })
  }

  return <>{formatText(text)}</>
}

// Action Confirmation Card
function ActionCard({ type, data, onAction }) {
  if (type === 'cart_added') {
    return (
      <div className="action-card success">
        <div className="action-icon">✅</div>
        <div className="action-content">
          <h4>Added to Cart!</h4>
          <p>{data.product_name} x{data.quantity}</p>
          <div className="action-buttons">
            <button className="btn-secondary" onClick={() => onAction('continue')}>
              Continue Shopping
            </button>
            <button className="btn-primary" onClick={() => onAction('view_cart')}>
              View Cart ({data.cart_total_items})
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (type === 'order_placed') {
    return (
      <div className="action-card success">
        <div className="action-icon">🎉</div>
        <div className="action-content">
          <h4>Order Placed Successfully!</h4>
          <p className="order-id">Order ID: {data.order_id}</p>
          <p className="tracking-id">Tracking: {data.tracking_id}</p>
          <p className="delivery-date">Expected: {data.estimated_delivery}</p>
          <div className="action-buttons">
            <button className="btn-primary" onClick={() => onAction('track_order', data.order_id)}>
              Track Order
            </button>
          </div>
        </div>
      </div>
    )
  }

  return null
}

// Cart Summary Card
function CartCard({ items, total, onAction }) {
  return (
    <div className="cart-card">
      <div className="cart-header">
        <h4>🛒 Your Cart</h4>
        <span className="item-count">{items.length} items</span>
      </div>
      <div className="cart-items">
        {items.map((item, idx) => (
          <div key={idx} className="cart-item">
            <div className="item-info">
              <span className="item-name">{item.product_name}</span>
              <span className="item-qty">x{item.quantity}</span>
            </div>
            <span className="item-price">₹{item.total}</span>
          </div>
        ))}
      </div>
      <div className="cart-footer">
        <div className="cart-total">
          <span>Total:</span>
          <span className="total-amount">₹{total}</span>
        </div>
        <div className="cart-actions">
          <button className="btn-secondary" onClick={() => onAction('continue')}>
            Continue Shopping
          </button>
          <button className="btn-primary" onClick={() => onAction('checkout')}>
            Proceed to Checkout
          </button>
        </div>
      </div>
    </div>
  )
}

// Order Tracking Timeline
function OrderTracking({ order }) {
  const steps = [
    { status: 'Order Confirmed', date: order.order_date, completed: true },
    { status: 'Packed', date: order.packed_date, completed: order.status !== 'Confirmed' },
    { status: 'Shipped', date: order.shipped_date, completed: order.status === 'Shipped' || order.status === 'Delivered' },
    { status: 'Out for Delivery', date: order.delivery_date, completed: order.status === 'Delivered' },
    { status: 'Delivered', date: order.estimated_delivery, completed: order.status === 'Delivered' }
  ]

  return (
    <div className="order-tracking">
      <div className="tracking-header">
        <h4>📦 Order Tracking</h4>
        <p className="tracking-id">Tracking ID: {order.tracking_id}</p>
      </div>
      <div className="tracking-timeline">
        {steps.map((step, idx) => (
          <div key={idx} className={`timeline-step ${step.completed ? 'completed' : 'pending'}`}>
            <div className="step-marker">
              {step.completed ? '✓' : idx + 1}
            </div>
            <div className="step-content">
              <div className="step-status">{step.status}</div>
              {step.date && <div className="step-date">{step.date}</div>}
            </div>
            {idx < steps.length - 1 && <div className="step-line"></div>}
          </div>
        ))}
      </div>
      <div className="tracking-footer">
        <p className="delivery-estimate">
          Expected Delivery: <strong>{order.estimated_delivery}</strong>
        </p>
      </div>
    </div>
  )
}

// Login Form Component
function LoginForm({ onSuccess, onSwitchToRegister }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await fetch(`${API_BASE}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })

      const data = await response.json()

      if (response.ok) {
        onSuccess(data.access_token, data.user)
      } else {
        setError(data.detail || 'Login failed')
      }
    } catch (err) {
      setError('Connection error. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chat-form">
      <h3>🔐 Login to Continue</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {error && <div className="error-msg">{error}</div>}
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
        <button type="button" className="link-btn" onClick={onSwitchToRegister}>
          Don't have an account? Register
        </button>
      </form>
    </div>
  )
}

// Register Form Component
function RegisterForm({ onSuccess, onSwitchToLogin }) {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    full_name: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await fetch(`${API_BASE}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      const data = await response.json()

      if (response.ok) {
        onSuccess(data.access_token, data.user)
      } else {
        setError(data.detail || 'Registration failed')
      }
    } catch (err) {
      setError('Connection error. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chat-form">
      <h3>📝 Create Account</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Full Name"
          value={formData.full_name}
          onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Username"
          value={formData.username}
          onChange={(e) => setFormData({ ...formData, username: e.target.value })}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={formData.password}
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          required
        />
        {error && <div className="error-msg">{error}</div>}
        <button type="submit" disabled={loading}>
          {loading ? 'Creating account...' : 'Register'}
        </button>
        <button type="button" className="link-btn" onClick={onSwitchToLogin}>
          Already have an account? Login
        </button>
      </form>
    </div>
  )
}

export default function ChatWidget({ autoOpen = false, initialMessage = '' }) {
  const { user, token, login, logout, isAuthenticated } = useAuth()
  const [open, setOpen] = useState(autoOpen)
  const [showAuthForm, setShowAuthForm] = useState(null)
  const [messages, setMessages] = useState([
    { text: 'Hi there! 👋 Welcome to AJ Creations!', role: 'ai', time: Date.now() },
    { text: 'How can I help you with your shopping today?', role: 'ai', time: Date.now() },
  ])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef(null)
  const textareaRef = useRef(null)

  const [userId] = useState(() => {
    const saved = localStorage.getItem('chat_user_id')
    if (saved) return saved
    const newId = `uid-${Math.floor(Math.random() * 1000000)}`
    localStorage.setItem('chat_user_id', newId)
    return newId
  })

  useEffect(() => {
    if (autoOpen) {
      setOpen(true)
      if (initialMessage) {
        setInput(initialMessage)
      }
    }
  }, [autoOpen, initialMessage])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    const root = document.getElementById('app-root')
    if (!root) return
    root.classList.toggle('chat-open', open)
  }, [open])

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px'
    }
  }, [input])

  const handleAuthSuccess = (accessToken, userData) => {
    login(accessToken, userData)
    setShowAuthForm(null)
    setMessages(prev => [...prev, {
      text: `Welcome back, ${userData.username}! 🎉 You're now logged in.`,
      role: 'ai',
      time: Date.now()
    }])
  }

  const handleAction = async (action, data) => {
    if (action === 'view_cart') {
      await sendMessage('Show my cart')
    } else if (action === 'checkout') {
      await sendMessage('Place my order')
    } else if (action === 'track_order') {
      await sendMessage(`Track order ${data}`)
    } else if (action === 'continue') {
      // Just close the action card, do nothing
    }
  }

  const sendMessage = async (messageText = input.trim()) => {
    if (!messageText) return

    const userMessage = { text: messageText, role: 'user', time: Date.now() }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsTyping(true)

    try {
      const response = await fetch(`${API_BASE}/api/chat/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          ...(token && { 'Authorization': `Bearer ${token}` })
        },
        body: JSON.stringify({
          message: messageText,
          user_id: userId,
        }),
      })

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)

      const data = await response.json()

      const aiMessage = {
        text: data.reply || 'No response from server',
        role: 'ai',
        time: Date.now(),
        products: parseProductsFromResponse(data.reply),
        actionCard: parseActionCard(data.reply, messageText),
        cartData: parseCartData(data.reply),
        orderData: parseOrderData(data.reply),
        sources: data.sources,
        requiresAuth: data.reply.includes('login') || data.reply.includes('sign in')
      }

      setMessages(prev => [...prev, aiMessage])

      if (aiMessage.requiresAuth && !isAuthenticated) {
        setShowAuthForm('login')
      }
    } catch (error) {
      console.error('❌ Error:', error)
      setMessages(prev => [
        ...prev,
        { text: 'Sorry, I could not connect to the server. Please try again.', role: 'ai', time: Date.now(), error: true }
      ])
    } finally {
      setIsTyping(false)
    }
  }

  const parseProductsFromResponse = (text) => {
    const productRegex = /\d+\.\s+\*\*(.+?)\*\*\s+-\s+₹([\d,]+)/g
    const products = []
    let match

    while ((match = productRegex.exec(text)) !== null) {
      products.push({
        name: match[1],
        price: match[2]
      })
    }

    return products.length > 0 ? products : null
  }

  const parseActionCard = (text, userMessage) => {
    // Check if item was added to cart
    if (text.includes('Added') && text.includes('cart') || text.includes('Updated')) {
      const nameMatch = text.match(/(?:Added|Updated)\s+(.+?)\s+(?:to cart|quantity)/i)
      const qtyMatch = text.match(/quantity to (\d+)|x(\d+)/)
      const itemsMatch = text.match(/cart_total_items[:\s]+(\d+)|(\d+)\s+items/i)

      if (nameMatch) {
        return {
          type: 'cart_added',
          data: {
            product_name: nameMatch[1],
            quantity: qtyMatch ? (qtyMatch[1] || qtyMatch[2] || 1) : 1,
            cart_total_items: itemsMatch ? (itemsMatch[1] || itemsMatch[2] || 1) : 1
          }
        }
      }
    }

    // Check if order was placed
    if (text.includes('Order placed') || text.includes('Order ID')) {
      const orderIdMatch = text.match(/Order ID:\s*(\w+)/i) || text.match(/order_id[:\s]+(\w+)/i)
      const trackingMatch = text.match(/Tracking(?:\s+ID)?:\s*(\w+)/i) || text.match(/tracking_id[:\s]+(\w+)/i)
      const deliveryMatch = text.match(/(?:Expected|Estimated)(?:\s+Delivery)?:\s*([\d-]+)/i)

      if (orderIdMatch) {
        return {
          type: 'order_placed',
          data: {
            order_id: orderIdMatch[1],
            tracking_id: trackingMatch ? trackingMatch[1] : 'N/A',
            estimated_delivery: deliveryMatch ? deliveryMatch[1] : 'TBD'
          }
        }
      }
    }

    return null
  }

  const parseCartData = (text) => {
    // Parse cart items from response
    if (text.includes('Your cart') && text.includes('items:')) {
      const itemRegex = /•\s+(.+?)\s+x(\d+)\s+-\s+₹([\d,]+)/g
      const items = []
      let match

      while ((match = itemRegex.exec(text)) !== null) {
        items.push({
          product_name: match[1],
          quantity: parseInt(match[2]),
          total: parseInt(match[3].replace(/,/g, ''))
        })
      }

      const totalMatch = text.match(/\*\*Total:\s*₹([\d,]+)\*\*/i)

      if (items.length > 0) {
        return {
          items,
          total: totalMatch ? parseInt(totalMatch[1].replace(/,/g, '')) : 0
        }
      }
    }

    return null
  }

  const parseOrderData = (text) => {
    // Parse order tracking data
    if (text.includes('Order Tracking') || text.includes('Tracking ID')) {
      const trackingMatch = text.match(/Tracking ID:\s*(\w+)/i)
      const statusMatch = text.match(/current_status[:\s]+(\w+)/i)
      const deliveryMatch = text.match(/estimated_delivery[:\s]+([\d-]+)/i)

      if (trackingMatch) {
        return {
          tracking_id: trackingMatch[1],
          status: statusMatch ? statusMatch[1] : 'Confirmed',
          estimated_delivery: deliveryMatch ? deliveryMatch[1] : 'TBD',
          order_date: new Date().toISOString().split('T')[0]
        }
      }
    }

    return null
  }

  const handleAddToCart = async (productName) => {
    if (!isAuthenticated) {
      setShowAuthForm('login')
      setMessages(prev => [...prev, {
        text: 'Please login to add items to your cart.',
        role: 'ai',
        time: Date.now()
      }])
      return
    }

    await sendMessage(`Add ${productName} to cart`)
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
        💬 Chat with us
      </button>
    )
  }

  return (
    <div className="chat-widget-container">
      <div className="chat-header-custom">
        <div className="header-left">
          <div className="header-avatar">🛍️</div>
          <div className="header-title">
            AJ Creations Assistant
            {isAuthenticated && <span className="user-badge">• {user?.username}</span>}
          </div>
        </div>
        <button onClick={() => setOpen(false)} className="chat-close-btn">
          ✕
        </button>
      </div>

      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className="message-wrapper-custom">
            <div className={`message-bubble-custom ${msg.role}`}>
              <MessageFormatter text={msg.text} />
            </div>

            {/* Product Cards */}
            {msg.products && msg.products.length > 0 && (
              <div className="product-cards">
                {msg.products.map((product, pidx) => (
                  <div key={pidx} className="product-card">
                    <div className="product-info">
                      <div className="product-name">{product.name}</div>
                      <div className="product-price">₹{product.price}</div>
                    </div>
                    <button
                      className="product-add-btn"
                      onClick={() => handleAddToCart(product.name)}
                    >
                      Add to Cart
                    </button>
                  </div>
                ))}
              </div>
            )}

            {/* Action Cards */}
            {msg.actionCard && (
              <ActionCard
                type={msg.actionCard.type}
                data={msg.actionCard.data}
                onAction={handleAction}
              />
            )}

            {/* Cart Summary */}
            {msg.cartData && (
              <CartCard
                items={msg.cartData.items}
                total={msg.cartData.total}
                onAction={handleAction}
              />
            )}

            {/* Order Tracking */}
            {msg.orderData && (
              <OrderTracking order={msg.orderData} />
            )}
          </div>
        ))}

        {/* Auth Forms */}
        {showAuthForm === 'login' && (
          <div className="message-wrapper-custom">
            <LoginForm
              onSuccess={handleAuthSuccess}
              onSwitchToRegister={() => setShowAuthForm('register')}
            />
          </div>
        )}

        {showAuthForm === 'register' && (
          <div className="message-wrapper-custom">
            <RegisterForm
              onSuccess={handleAuthSuccess}
              onSwitchToLogin={() => setShowAuthForm('login')}
            />
          </div>
        )}

        {isTyping && (
          <div className="message-wrapper-custom">
            <div className="message-bubble-custom ai typing">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <textarea
          ref={textareaRef}
          className="chat-input-field"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          rows={1}
          disabled={isTyping}
        />
        <button
          onClick={() => sendMessage()}
          className="chat-send-btn"
          disabled={isTyping || !input.trim()}
        >
          ➤
        </button>
      </div>
    </div>
  )
}
