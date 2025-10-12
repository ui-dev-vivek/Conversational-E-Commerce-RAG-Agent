import { useEffect, useRef, useState } from 'react'

export default function ChatWidget() {
  const [open, setOpen] = useState(true)
  const [authenticated, setAuthenticated] = useState(false)
  const [profile, setProfile] = useState({ name: '', email: '' })
  const [messages, setMessages] = useState([])
  const [text, setText] = useState('')
  const bodyRef = useRef(null)

  useEffect(() => {
    // auto-open and show login first
    setOpen(true)
  }, [])

  useEffect(() => {
    // auto-scroll to bottom when messages change
    if (bodyRef.current) {
      bodyRef.current.scrollTop = bodyRef.current.scrollHeight
    }
  }, [messages])

  function login(e) {
    e?.preventDefault()
    if (!profile.name.trim() || !profile.email.trim()) return
    setAuthenticated(true)
    // greet the user
    setTimeout(() => {
      setMessages([{ from: 'bot', text: `Hi ${profile.name}, How can I help you today?` }])
    }, 400)
  }

  function send() {
    if (!text.trim()) return
    const userMsg = { from: 'user', text: text.trim(), time: Date.now() }
    setMessages((m) => [...m, userMsg])
    setText('')
    // fake bot reply for demo
    setTimeout(() => {
      setMessages((m) => [...m, { from: 'bot', text: "I'll look into that — can you share more details?" }])
    }, 700)
  }

  if (!open) {
    return (
      <button onClick={() => setOpen(true)} className="chat-open-btn">Chat</button>
    )
  }

  return (
    <div className="chat-widget chat-large" aria-hidden={!open}>
      <div className="chat-header">
        <div><div className="avatar">A</div> {authenticated ? profile.name : 'Assistant'}</div>
        <div>
          <button onClick={() => setOpen(false)} className="chat-close">✕</button>
        </div>
      </div>

      {!authenticated ? (
        <div className="chat-auth">
          <h4>Welcome</h4>
          <p>Please login or create an account to start chatting</p>
          <form onSubmit={login} className="auth-form">
            <input value={profile.name} onChange={(e)=>setProfile(p=>({...p,name:e.target.value}))} placeholder="Full name" />
            <input value={profile.email} onChange={(e)=>setProfile(p=>({...p,email:e.target.value}))} placeholder="Email" />
            <div className="auth-actions">
              <button className="primary" onClick={login}>Continue</button>
            </div>
          </form>
        </div>
      ) : (
        <>
          <div className="chat-body" ref={bodyRef}>
            {messages.length === 0 && (
              <div className={`chat-bubble bot`}>
                <div className="bubble-card">Hello</div>
              </div>
            )}
            {messages.map((m, i) => (
              <div key={i} className={`chat-bubble ${m.from === 'bot' ? 'bot' : 'user'}`} style={{alignSelf: m.from === 'bot' ? 'flex-start' : 'flex-end'}}>
                <div className="bubble-card {m.from}">{m.text}</div>
              </div>
            ))}
          </div>

          <div className="chat-input">
            <input value={text} onChange={(e) => setText(e.target.value)} placeholder="Type a message" onKeyDown={(e)=>{ if(e.key==='Enter') send() }} />
            <button onClick={send} className="primary">Send</button>
          </div>
        </>
      )}
    </div>
  )
}
