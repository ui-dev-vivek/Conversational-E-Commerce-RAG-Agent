# 🧠 AI-Powered E-Commerce Chat Assistant

**An intelligent conversational AI assistant for e-commerce that allows users to browse products, track orders, and make purchases through natural chat interactions.**

## 📖 Project Description

This is an end-to-end **E-Commerce Conversational AI Assistant** that combines the power of **RAG (Retrieval-Augmented Generation)** and **AI Agents** to create a seamless shopping experience. Instead of traditional navigation, users can simply chat with the AI to find products, check order status, and complete purchases.

### 🎯 Key Features
- **🛒 Smart Product Discovery**: "Show me red t-shirts under ₹500" or "Find laptops with 16GB RAM"
- **📦 Order Management**: "Where is my latest order?" or "Show my order history"
- **🧾 Conversational Checkout**: Add items to cart and complete purchases through chat
- **👤 Personalized Experience**: User authentication and session management
- **💬 Intelligent Dialog**: Context-aware conversations that understand both products and user context



## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend** | React + Chat UI (`react-chat-elements`) |
| **Backend** | FastAPI with LangChain / RAG pipeline | Agentic behavior with LangGraph |
| **Database** | PostgreSQL / SQLite + ChromaDB |
| **Embeddings** | `sentence-transformers/all-MiniLM-L6-v2` |
| **LLM** | OpenRouter (gpt-sso) |

---

## 🧭 Project Roadmap

### **Phase 1: Core Setup**
1. Create **FastAPI Backend**
   - `/api/auth` → login/register
   - `/api/orders` → CRUD for orders
   - `/api/products` → product listing
   - `/api/chat` → handles LLM chat (RAG-powered)
2. Setup **React Frontend**
   - Login/Signup, Product listing, Order tracking, Chat screen
3. Setup **RAG**
   - Product data & FAQs → ChromaDB
   - Use MiniLM embeddings for retrieval

### **Phase 2: Smart Chat Integration**
- Handle chat intents (order tracking, product browsing)
- RAG decides between retrieval or API calls

### **Phase 3: Add Agentic Behavior**
- Add **LangGraph / LangChain Agent** with tools:
  - `ProductSearchTool`
  - `OrderStatusTool`
  - `PlaceOrderTool`

### **Phase 4: Polish & Deploy**
- Add authentication & conversation memory
- Enhance chat UI
- Deploy Frontend (Vercel) & Backend (Render/AWS/Railway)

---


## 📁 Folder Structure

```
ec-chat/
│
├── server/                          # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── create_tables.py        # DB initialization script
│   │   ├── config/                 # Configuration
│   │   │   ├── __init__.py
│   │   │   ├── settings.py         # Pydantic settings (env vars)
│   │   │   └── database.py         # SQLAlchemy setup
│   │   ├── models/                 # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   └── models.py           # User, Product, Order, etc.
│   │   ├── schemas/                # Pydantic request/response schemas
│   │   │   ├── __init__.py
│   │   │   └── schemas.py
│   │   ├── routes/                 # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py             # /api/auth
│   │   │   ├── products.py         # /api/products
│   │   │   ├── orders.py           # /api/orders
│   │   │   └── chat.py             # /api/chat (RAG-powered)
│   │   ├── services/               # Business logic layer
│   │   │   └── __init__.py
│   │   ├── utils/                  # Helper functions
│   │   │   ├── __init__.py
│   │   │   └── auth.py             # JWT, password hashing
│   │   └── rag/                    # RAG & LLM components
│   │       ├── __init__.py
│   │       ├── embedder.py         # sentence-transformers
│   │       ├── retriever.py        # ChromaDB vector search
│   │       └── agent_tools.py      # LangChain tools
│   ├── run.py                      # Development server runner
│   ├── requirements.txt            # Python dependencies
│   ├── .env                        # Environment variables (git-ignored)
│   └── .env.example                # Example env file
│
└── client/                          # React Frontend
    ├── src/
    │   ├── components/
    │   │   └── ChatUI/
    │   ├── pages/
    │   │   ├── Login.jsx
    │   │   ├── Orders.jsx
    │   │   ├── Products.jsx
    │   │   └── Chat.jsx
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── api/                    # API client helpers
    ├── package.json
    └── vite.config.js
```

---


## 💬 Free React Chat UI Libraries

| Library | Link | Notes |
|----------|------|-------|
| **react-chat-elements** | https://github.com/Detaysoft/react-chat-elements | Easiest to use, customizable |
| **react-chat-widget** | https://github.com/Wolox/react-chat-widget | Minimalist floating chat box |
| **Vercel’s next-chat-ui** | https://github.com/vercel/ai-chatbot | Modern & production-grade |
| **Chat UI Kit** | https://github.com/GetStream/stream-chat-react | Free tier available |

**Recommendation:** Start with `react-chat-elements` → later upgrade to `next-chat-ui`.

---

## 🧠 Free Embedding Models

| Model | Type | Notes |
|--------|------|--------|
| `sentence-transformers/all-MiniLM-L6-v2` | Local | Fast, free, great for e-commerce |
| `BAAI/bge-small-en-v1.5` | Local | Multilingual support |
| `text-embedding-3-small` | API | High-quality (OpenAI) |

**Start with:** `MiniLM-L6-v2` (no API cost).

---

## 🧱 Example Commands

### **Setup Backend**
```bash
cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### **Setup Frontend**
```bash
cd client
npm install
npm run dev
```

---

## ✨ Deployment
- **Frontend:** Vercel / Netlify  
- **Backend:** Render / Railway / AWS EC2  
- **Vector DB:** Chroma (local) or Pinecone (cloud)

---

## 📘 Author
**Vivek Yadav** — Agentic AI & RAG Developer  
+917619876249