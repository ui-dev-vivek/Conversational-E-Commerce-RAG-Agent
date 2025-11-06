# Project Structure Tree

```
server/
│
├── 📂 app/                          # Main Application Package
│   │
│   ├── 🎛️ core/
│   │   ├── __init__.py
│   │   ├── config.py                # ⭐ Load env vars, DB, LLM, RAG settings
│   │   └── constants.py             # Global constants
│   │
│   ├── 🧠 rag/                      # RAG PIPELINE
│   │   ├── __init__.py
│   │   ├── 🔢 embeddings/
│   │   │   ├── __init__.py
│   │   │   ├── embedding_factory.py
│   │   │   └── local_embedder.py    # MiniLM-L6-v2 embeddings
│   │   │
│   │   ├── 💾 vectorstore/
│   │   │   ├── __init__.py
│   │   │   ├── chroma_store.py      # ChromaDB
│   │   │   └── store_factory.py
│   │   │
│   │   ├── 🔍 retrievers/
│   │   │   ├── __init__.py
│   │   │   ├── base_retriever.py
│   │   │   ├── similarity_retriever.py
│   │   │   └── hybrid_retriever.py
│   │   │
│   │   └── 💬 prompts/
│   │       ├── __init__.py
│   │       ├── system_prompts.py
│   │       └── prompt_templates.py
│   │
│   ├── 🤖 agents/                   # AGENT ORCHESTRATION
│   │   ├── __init__.py
│   │   ├── ⚙️ tools/                # AGENT TOOLS
│   │   │   ├── __init__.py
│   │   │   ├── base_tool.py
│   │   │   ├── product_tools.py     # SearchProducts, GetDetails
│   │   │   ├── order_tools.py       # GetStatus, ListOrders
│   │   │   ├── cart_tools.py        # AddCart, Checkout
│   │   │   ├── user_tools.py        # GetProfile, UpdateAddress
│   │   │   ├── currency_tool.py     # Convert, Format
│   │   │   └── tool_registry.py     # Central registry
│   │   │
│   │   └── 🔗 chains/
│   │       ├── __init__.py
│   │       ├── rag_chain.py         # RAG execution
│   │       ├── agent_executor.py    # LangGraph agent
│   │       └── routing_chain.py     # Intent routing
│   │
│   ├── 💾 memory/                   # CONVERSATION MEMORY
│   │   ├── __init__.py
│   │   ├── 📝 chat_history/
│   │   │   ├── __init__.py
│   │   │   ├── base_history.py
│   │   │   ├── database_history.py  # SQL persistence
│   │   │   └── memory_history.py    # In-memory
│   │   └── context_manager.py       # Context window mgmt
│   │
│   ├── 🔧 services/                 # BUSINESS LOGIC LAYER
│   │   ├── __init__.py
│   │   ├── 🧠 llm/
│   │   │   ├── __init__.py
│   │   │   ├── base_llm.py
│   │   │   └── llm_factory.py       # OpenRouter, Anthropic, local
│   │   │
│   │   ├── 🧠 rag/
│   │   │   ├── __init__.py
│   │   │   ├── rag_pipeline.py      # Orchestrate RAG
│   │   │   └── document_processor.py # Chunking & cleaning
│   │   │
│   │   └── 🤖 agent/
│   │       ├── __init__.py
│   │       └── agent_service.py     # Orchestrate agents
│   │
│   ├── 📡 routes/                   # API ENDPOINTS
│   │   ├── __init__.py
│   │   ├── auth.py                  # /api/auth/*
│   │   ├── products.py              # /api/products/*
│   │   ├── orders.py                # /api/orders/*
│   │   └── chat.py                  # /api/chat/* ⭐ MAIN
│   │
│   ├── 🗄️ models/
│   │   ├── __init__.py
│   │   └── models.py                # User, Product, Order models
│   │
│   ├── 📋 schemas/
│   │   ├── __init__.py
│   │   └── schemas.py               # Pydantic request/response
│   │
│   ├── 🗝️ config/
│   │   ├── __init__.py
│   │   ├── database.py              # SQLAlchemy setup
│   │   └── settings.py              # ⚠️ DEPRECATED (use core/config.py)
│   │
│   ├── 🛠️ utils/
│   │   ├── __init__.py
│   │   └── auth.py                  # JWT, password hashing
│   │
│   ├── ⚠️ exceptions/
│   │   ├── __init__.py
│   │   └── base_exceptions.py       # Custom exceptions
│   │
│   ├── ✅ validators/
│   │   ├── __init__.py
│   │   └── input_validators.py      # Input validation
│   │
│   ├── 📌 constants/
│   │   ├── __init__.py
│   │   ├── messages.py              # Messages & error strings
│   │   └── enums.py                 # OrderStatus, UserRole
│   │
│   ├── 🔄 middlewares/
│   │   ├── __init__.py
│   │   ├── error_handler.py         # Global exception handling
│   │   └── logging_middleware.py    # Request/response logging
│   │
│   ├── 📝 logging_config/
│   │   ├── __init__.py
│   │   └── logger.py                # Structured logging
│   │
│   ├── 🔗 dependencies/
│   │   ├── __init__.py
│   │   └── injections.py            # DI: DB, LLM, RAG, agent
│   │
│   └── 🚀 main.py                   # FastAPI app creation
│
├── ✔️ tests/
│   ├── conftest.py                  # Pytest config
│   ├── unit/                        # Unit tests
│   │   └── __init__.py
│   ├── integration/                 # Integration tests
│   │   └── __init__.py
│   └── fixtures/                    # Test data
│       ├── __init__.py
│       └── mock_data.py
│
├── 🔄 migrations/                   # DB version control
│   └── README.md
│
├── 🎯 scripts/
│   ├── README.md
│   ├── init_db.py                   # Initialize database
│   └── populate_embeddings.py       # Index to ChromaDB
│
├── 📂 data/
│   ├── README.md
│   ├── products.json                # Product catalog
│   └── faqs.json                    # FAQ documents
│
├── 📋 logs/
│   ├── README.md
│   ├── app.log
│   └── error.log
│
├── 🚀 run.py                        # Entry point
├── 📦 requirements.txt              # Dependencies
├── .env                             # Env vars (git-ignored)
├── .env.example                     # Env template
└── ℹ️ INFO.md                        # This file

---

## 📌 Quick Reference

### ⭐ KEY FOLDERS:

1. **`app/core/`** - App configuration & constants
2. **`app/rag/`** - Embeddings, vectors, retrievers, prompts
3. **`app/agents/`** - Tools & agent execution (LangGraph)
4. **`app/memory/`** - Conversation history storage
5. **`app/services/`** - Orchestration services (RAG, Agent, LLM)
6. **`app/routes/`** - API endpoints
7. **`app/models/`** - Database schema
8. **`app/schemas/`** - Request/response validation

### 🔄 FLOW:

**Chat Message**
```
Frontend → routes/chat.py 
         → agents/chains/routing_chain.py (intent routing)
         → agents/chains/agent_executor.py (if tool needed)
         → agents/tools/* (execute tool)
         → services/llm (generate response)
         → memory/chat_history (save conversation)
         → Frontend
```

**RAG Query**
```
Frontend → routes/chat.py
         → services/rag/rag_pipeline.py
         → rag/retrievers/* (semantic search)
         → services/llm (answer with context)
         → Frontend
```
