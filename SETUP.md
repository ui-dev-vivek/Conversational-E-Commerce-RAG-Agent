# E-Commerce Chat Assistant - Setup & Testing Guide

## ✅ What's Implemented

### Backend (FastAPI)

- **Chat endpoint**: `POST /api/chat/message`
  - Accepts: `{ "message": "user text" }`
  - Returns: `{ "reply": "bot response" }`
- **CORS**: Configured to allow all origins (for development)
- **Database**: SQLite fallback for local development
- **Other endpoints**: Auth, Products, Orders (placeholder implementations)

### Frontend (React + Deep Chat)

- **Deep Chat UI**: Premium chat widget using `deep-chat-react` library
- **Custom styling**: Gradient header, modern message bubbles, smooth animations
- **API integration**: Connects to backend at `http://localhost:8000/api/chat/message`
- **Request/Response transformation**: Automatically converts between Deep Chat and backend formats

## 🚀 Quick Start

### 1. Start the Backend

```bash
cd server
python run.py
```

Backend will run at: **http://localhost:8000**

API docs available at: **http://localhost:8000/docs**

### 2. Start the Frontend

```bash
cd client
npm install  # if not already done
npm run dev
```

Frontend will run at: **http://localhost:5174** (or 5173 if available)

## 🧪 Test the API

### Using cURL:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/chat/message' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "message": "hi"
}'
```

**Expected Response:**

```json
{
  "reply": "I received your message: 'hi'. How can I help you with our products?"
}
```

### Using the UI:

1. Open **http://localhost:5174** in your browser
2. You'll see the chat widget open automatically
3. Type a message and press Enter (or click Send)
4. The bot will respond with an echo of your message

## 🔧 Configuration

### Frontend Environment Variables

Create `client/.env.local`:

```env
VITE_API_BASE=http://localhost:8000
```

### Backend Environment Variables

Create `server/.env`:

```env
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ecommerce_db
DEBUG=true
```

_Note: If DB credentials are not provided, SQLite will be used as fallback._

## 📁 Project Structure

```
ec-chat/
├── client/                    # React frontend
│   ├── src/
│   │   ├── ChatWidget.jsx    # Deep Chat component
│   │   ├── ChatWidget.css    # Custom styles
│   │   └── api/
│   │       └── index.js      # Axios wrapper (currently not used with Deep Chat)
│   └── package.json
│
└── server/                    # FastAPI backend
    ├── app/
    │   ├── main.py           # FastAPI app factory
    │   ├── routes/           # API endpoints
    │   │   ├── auth.py
    │   │   ├── products.py
    │   │   ├── orders.py
    │   │   └── chat.py       # Chat endpoint ✅
    │   ├── models/           # SQLAlchemy models
    │   ├── schemas/          # Pydantic schemas
    │   └── config/           # Settings & database
    └── run.py               # Server runner
```

## 🎨 Deep Chat Features

The chat widget includes:

- ✅ **Custom styling**: Purple gradient header, modern UI
- ✅ **Message history**: Initial greeting messages
- ✅ **Auto-scrolling**: Stays at bottom as messages arrive
- ✅ **Custom avatars**: Shop emoji for bot, user avatar for user
- ✅ **Smooth animations**: Typing indicators, transitions
- ✅ **Responsive**: Works on mobile and desktop
- ✅ **Backend integration**: Sends requests to `/api/chat/message`

## 🔄 How It Works

### Request Flow:

1. **User types message** in Deep Chat widget
2. **Deep Chat** sends request with message text
3. **Request Interceptor** transforms to: `{ message: "user text" }`
4. **Backend** receives message, processes it (currently echoes)
5. **Backend** returns: `{ reply: "bot response" }`
6. **Response Interceptor** transforms to: `{ text: "bot response", role: "ai" }`
7. **Deep Chat** displays the response in the chat

### Code Snippets:

**Frontend (ChatWidget.jsx):**

```javascript
const requestInterceptor = (requestDetails) => {
  const body = JSON.parse(requestDetails.body || "{}");
  const userMessage =
    body.messages?.[body.messages.length - 1]?.text || body.text || "";

  requestDetails.body = JSON.stringify({ message: userMessage });
  return requestDetails;
};

const responseInterceptor = (response) => {
  if (response.reply) {
    return { text: response.reply, role: "ai" };
  }
  return { text: "Sorry, I did not understand that.", role: "ai" };
};
```

**Backend (chat.py):**

```python
class ChatMessage(BaseModel):
    message: str

@router.post("/message")
async def chat_message(payload: ChatMessage):
    user_message = payload.message
    bot_reply = f"I received your message: '{user_message}'. How can I help you with our products?"
    return {"reply": bot_reply}
```

## 📝 Next Steps

To make this production-ready:

1. **Integrate RAG + LLM** in `server/app/routes/chat.py`
2. **Add authentication** (JWT tokens)
3. **Connect to MySQL** for production database
4. **Add message persistence** (save chat history to DB)
5. **Implement product search** and recommendations
6. **Add streaming responses** for better UX
7. **Deploy backend** (e.g., on Railway, Render, or AWS)
8. **Deploy frontend** (e.g., on Vercel, Netlify)

## 🐛 Troubleshooting

### Backend not starting?

- Check if port 8000 is available
- Verify Python dependencies are installed: `pip install -r requirements.txt`

### Frontend not connecting?

- Ensure backend is running at `http://localhost:8000`
- Check browser console for CORS errors
- Verify `VITE_API_BASE` environment variable

### Deep Chat not showing?

- Check if `deep-chat-react` is installed: `npm list deep-chat-react`
- Open browser DevTools and check for React errors

## 📚 Resources

- [Deep Chat Documentation](https://deepchat.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
