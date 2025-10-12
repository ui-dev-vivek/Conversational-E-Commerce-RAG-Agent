
# 🧠 AI-Powered E-Commerce Chat Assistant (RAG + Agents)

An end-to-end **E-Commerce Conversational AI Assistant** built using **FastAPI** (backend) and **React** (frontend).  
Users can browse products, track orders, and place new ones via chat.

---

## 🚀 Project Overview

### User Capabilities
- 🛒 Browse or search products via chat (“Show me red t-shirts under ₹500”)
- 📦 Track existing orders (“Where is my latest order?”)
- 🧾 Place new orders (chat → cart → checkout)
- 👤 Login & maintain session
- 💬 Chat with an intelligent agent that understands both product catalog & user profile.

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend** | React + Chat UI (`react-chat-elements`) |
| **Backend** | FastAPI with LangChain / RAG pipeline |
| **Database** | PostgreSQL / SQLite + ChromaDB |
| **Embeddings** | `sentence-transformers/all-MiniLM-L6-v2` |
| **LLM** | OpenAI / Ollama (local LLMs like Mistral, Llama3) |

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

## 🧩 Next Steps

1. Generate FastAPI + React skeleton
2. Connect `/chat` API endpoint with RAG logic
3. Integrate `react-chat-elements`
4. Add embeddings + ChromaDB
5. Extend with LangChain Agent Tools

---

## 🧱 Example Commands

### **Setup Backend**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### **Setup Frontend**
```bash
cd frontend
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