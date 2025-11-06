# 📖 Complete Project Index & Documentation Map

## 🎯 Start Here - Reading Order

| # | Document | Time | Purpose |
|---|----------|------|---------|
| 1️⃣ | **THIS FILE** | 5 min | Overview & index |
| 2️⃣ | `QUICKSTART.md` | 5 min | Get running immediately |
| 3️⃣ | `STRUCTURE.md` | 10 min | Visual reference |
| 4️⃣ | `INFO.md` | 30 min | Complete documentation |
| 5️⃣ | `MIGRATION.md` | 15 min | Move existing code |
| 6️⃣ | `RESTRUCTURE_SUMMARY.md` | 10 min | Summary of changes |
| 7️⃣ | `VERIFICATION_CHECKLIST.md` | 5 min | Verify completion |

---

## 📁 Directory Structure & Responsibilities

### **ROOT LEVEL** (`server/`)
```
server/
├── app/              ← Your application code (refactored)
├── tests/            ← Test suite (unit, integration)
├── scripts/          ← Utility scripts
├── data/             ← Seed data & knowledge base
├── logs/             ← Application logs
├── migrations/       ← Database migrations
├── run.py            ← Development server entry point
├── requirements.txt  ← Python dependencies
├── .env              ← Environment variables (git-ignored)
├── .env.example      ← .env template
└── *.md              ← Documentation guides
```

---

## 🏗️ App Structure (Layer by Layer)

### **LAYER 1: API & Routes** (`app/routes/`)
| File | Endpoints | Purpose |
|------|-----------|---------|
| `auth.py` | `/api/auth/login`, `/register` | User authentication |
| `products.py` | `/api/products/{id}`, `/search` | Product browsing |
| `orders.py` | `/api/orders`, `/orders/{id}` | Order management |
| `chat.py` | **`POST /api/chat/message`** | ⭐ Main chat endpoint |

**→ Read**: `INFO.md` → Search for "routes/"

---

### **LAYER 2: Orchestration** (`app/services/`)

#### `llm/` - LLM Management
| File | Purpose |
|------|---------|
| `base_llm.py` | Abstract LLM interface |
| `llm_factory.py` | Factory to create LLM instances |

#### `rag/` - RAG Pipeline
| File | Purpose |
|------|---------|
| `rag_pipeline.py` | Complete RAG orchestration |
| `document_processor.py` | Document chunking & cleaning |

#### `agent/` - Agent Service
| File | Purpose |
|------|---------|
| `agent_service.py` | High-level agent orchestration |

**→ Read**: `INFO.md` → Search for "services/"

---

### **LAYER 3: Core Components**

#### **3A. RAG Pipeline** (`app/rag/`)
```
rag/
├── embeddings/
│   ├── base_embedder.py      ← Abstract interface
│   ├── local_embedder.py     ← MiniLM-L6-v2 implementation
│   └── embedding_factory.py  ← Factory for embedders
├── vectorstore/
│   ├── chroma_store.py       ← ChromaDB implementation
│   └── store_factory.py      ← Factory for vector stores
├── retrievers/
│   ├── base_retriever.py     ← Abstract interface
│   ├── similarity_retriever.py  ← Semantic search
│   └── hybrid_retriever.py   ← BM25 + semantic
└── prompts/
    ├── system_prompts.py     ← Role-based system messages
    └── prompt_templates.py   ← LangChain templates
```

**Flow**: Text → Embeddings → VectorStore → Retriever → Context → LLM

**→ Read**: `INFO.md` → Search for "rag/"

---

#### **3B. Agent System** (`app/agents/`)
```
agents/
├── tools/
│   ├── base_tool.py              ← Abstract tool interface
│   ├── product_tools.py          ← SearchProducts, Details
│   ├── order_tools.py            ← GetStatus, ListOrders
│   ├── cart_tools.py             ← AddCart, Checkout
│   ├── user_tools.py             ← Profile, Address
│   ├── currency_tool.py          ← Convert, Format
│   └── tool_registry.py          ← Central registry
└── chains/
    ├── rag_chain.py              ← RAG execution
    ├── agent_executor.py         ← LangGraph agent
    └── routing_chain.py          ← Intent routing
```

**Flow**: Query → Intent Detection → Tool Selection → Tool Execution → Response

**→ Read**: `INFO.md` → Search for "agents/"

---

#### **3C. Memory Management** (`app/memory/`)
```
memory/
├── chat_history/
│   ├── base_history.py       ← Abstract interface
│   ├── database_history.py   ← SQL persistence
│   └── memory_history.py     ← Fast in-memory
└── context_manager.py        ← Context window management
```

**→ Read**: `INFO.md` → Search for "memory/"

---

### **LAYER 4: Infrastructure**

#### Exception Handling (`app/exceptions/`)
```
exceptions/
├── base_exceptions.py
│   ├── RAGException
│   ├── AgentException
│   ├── ToolException
│   └── ValidationException
```

**→ Read**: `INFO.md` → Search for "exceptions/"

---

#### Validation (`app/validators/`)
```
validators/
├── input_validators.py
│   ├── validate_message()
│   ├── validate_query()
│   └── sanitize_input()
```

**→ Read**: `INFO.md` → Search for "validators/"

---

#### Constants (`app/constants/`)
```
constants/
├── messages.py          ← Error & success messages
└── enums.py            ← OrderStatus, UserRole, etc.
```

**→ Read**: `INFO.md` → Search for "constants/"

---

#### Middleware (`app/middlewares/`)
```
middlewares/
├── error_handler.py        ← Global exception handling
└── logging_middleware.py   ← Request/response logging
```

**→ Read**: `INFO.md` → Search for "middlewares/"

---

#### Configuration (`app/core/`)
```
core/
├── config.py           ← ⭐ All settings via Pydantic
└── constants.py        ← Global constants
```

**→ Read**: `INFO.md` → Search for "core/"

---

#### Dependency Injection (`app/dependencies/`)
```
dependencies/
└── injections.py   ← Provides: DB, LLM, RAG, Agent
```

**→ Read**: `INFO.md` → Search for "dependencies/"

---

### **LAYER 5: Data Models & Validation**

#### Database Models (`app/models/`)
```
models/
└── models.py
    ├── User          ← User accounts
    ├── Product       ← Product catalog
    ├── Order         ← Orders
    ├── OrderItem     ← Line items
    ├── Category      ← Product categories
    └── Address       ← Shipping addresses
```

**→ Read**: `INFO.md` → Search for "models/"

---

#### Request/Response Schemas (`app/schemas/`)
```
schemas/
└── schemas.py
    ├── ChatMessageRequest
    ├── ChatMessageResponse
    ├── ProductResponse
    ├── OrderSchema
    └── ...
```

**→ Read**: `INFO.md` → Search for "schemas/"

---

### **LAYER 6: Testing & Utilities**

#### Testing (`tests/`)
```
tests/
├── conftest.py           ← Pytest configuration
├── unit/                 ← Component tests
│   ├── test_embeddings.py
│   ├── test_retrievers.py
│   └── test_tools.py
├── integration/          ← Workflow tests
│   ├── test_rag_pipeline.py
│   └── test_agent_executor.py
└── fixtures/
    └── mock_data.py      ← Test data
```

**→ Read**: `INFO.md` → Search for "tests/"

---

#### Scripts (`scripts/`)
```
scripts/
├── init_db.py              ← Initialize database
└── populate_embeddings.py  ← Index products to ChromaDB
```

**→ Read**: `INFO.md` → Search for "scripts/"

---

#### Seed Data (`data/`)
```
data/
├── products.json         ← Product catalog (to create)
├── faqs.json            ← FAQ documents (to create)
└── knowledge_base/      ← Documentation files (to create)
```

**→ Read**: `INFO.md` → Search for "data/"

---

## 🔄 Request Processing Flow

### **Scenario 1: Tool-Based Request**
```
User: "Add red laptop to cart"
    ↓
POST /api/chat/message
    ↓
routes/chat.py
    ↓
RoutingChain (determine intent)
    ↓
AgentExecutor (LangGraph)
    ↓
AddToCartTool → Database
    ↓
LLM generates response
    ↓
Save to ChatHistory
    ↓
Return response
```

### **Scenario 2: RAG-Based Request**
```
User: "What's your return policy?"
    ↓
POST /api/chat/message
    ↓
routes/chat.py
    ↓
RoutingChain (determine intent)
    ↓
RAGPipeline:
  1. Embed query
  2. Search ChromaDB
  3. Retrieve documents
    ↓
LLM answers with context
    ↓
Save to ChatHistory
    ↓
Return response
```

**→ Read**: `INFO.md` → Search for "Request Flow"

---

## 🎯 Common Development Tasks

| Task | Location | Reference |
|------|----------|-----------|
| Add new tool | `app/agents/tools/` | QUICKSTART.md → Task 1 |
| Add new retriever | `app/rag/retrievers/` | QUICKSTART.md → Task 2 |
| Add new endpoint | `app/routes/` | QUICKSTART.md → Task 3 |
| Add new memory backend | `app/memory/chat_history/` | QUICKSTART.md → Task 4 |
| Add exception handling | `app/exceptions/` | INFO.md |
| Add validation | `app/validators/` | INFO.md |
| Write tests | `tests/` | QUICKSTART.md |
| Configure LLM | `app/core/config.py` | QUICKSTART.md |

**→ Read**: `QUICKSTART.md` for step-by-step tasks

---

## 🔗 Dependencies & Imports

### Key Import Paths

**For Routes:**
```python
from app.services.agent import AgentService
from app.services.rag import RAGPipeline
from app.memory.chat_history import DatabaseHistory
from app.core.config import Settings
```

**For Adding Tools:**
```python
from app.agents.tools.base_tool import BaseTool
from app.agents.tools.tool_registry import get_all_tools
```

**For Adding Retrievers:**
```python
from app.rag.retrievers.base_retriever import BaseRetriever
from app.rag.embeddings import LocalEmbedder
from app.rag.vectorstore import ChromaStore
```

**→ Read**: `MIGRATION.md` for detailed import mapping

---

## 📊 Architecture Patterns

| Pattern | Location | Purpose |
|---------|----------|---------|
| Factory | `*_factory.py` files | Create complex objects |
| Registry | `tool_registry.py` | Central management |
| DI (Dependency Injection) | `dependencies/injections.py` | Loose coupling |
| Abstract Base Classes | `base_*.py` files | Define interfaces |
| Service Layer | `services/` | Business logic |
| Middleware | `middlewares/` | Cross-cutting concerns |

**→ Read**: `INFO.md` → Search for "patterns"

---

## 🔐 Security & Configuration

### Environment Variables (`.env`)
```ini
DATABASE_URL=postgresql://...
LLM_API_KEY=...
LLM_MODEL=...
EMBEDDINGS_MODEL=all-MiniLM-L6-v2
SECRET_KEY=...
ALGORITHM=HS256
```

**→ Read**: `.env.example` for template

---

## 🧪 Testing Quick Reference

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/unit/test_tools.py -v

# Run with coverage
pytest tests/ --cov=app

# Run unit tests only
pytest tests/unit/ -v

# Run integration tests only
pytest tests/integration/ -v
```

**→ Read**: `QUICKSTART.md` → Testing Section

---

## 🚀 Deployment Checklist

- [ ] Read all documentation
- [ ] Move existing code using `MIGRATION.md`
- [ ] Initialize database: `python scripts/init_db.py`
- [ ] Populate embeddings: `python scripts/populate_embeddings.py`
- [ ] Run tests: `pytest tests/ -v`
- [ ] Start server: `python run.py`
- [ ] Visit docs: `http://localhost:8000/docs`
- [ ] Test API endpoints
- [ ] Deploy to production

**→ Read**: `QUICKSTART.md` → Starting the Server

---

## 📞 Finding Things

### **I want to find...**

| What | Where |
|------|-------|
| Folder structure | `STRUCTURE.md` |
| How to add a tool | `QUICKSTART.md` or `INFO.md` + search "tools" |
| LLM configuration | `app/core/config.py` or `QUICKSTART.md` |
| How to run tests | `QUICKSTART.md` |
| Database models | `app/models/models.py` or `INFO.md` |
| API endpoints | `app/routes/` or `INFO.md` |
| Error handling | `app/exceptions/` or `INFO.md` |
| Chat endpoint logic | `app/routes/chat.py` + `INFO.md` |
| RAG pipeline | `app/services/rag/` or `INFO.md` |
| Agent execution | `app/agents/chains/` or `INFO.md` |

---

## 📚 Documentation Summary

| File | Size | Topic | Read Time |
|------|------|-------|-----------|
| **INFO.md** | 19 KB | Complete reference | 30 min |
| **STRUCTURE.md** | 7.7 KB | Visual architecture | 10 min |
| **QUICKSTART.md** | 8.5 KB | Getting started | 5 min |
| **MIGRATION.md** | 7.6 KB | Moving code | 15 min |
| **RESTRUCTURE_SUMMARY.md** | 11 KB | What changed | 10 min |
| **VERIFICATION_CHECKLIST.md** | - | Completion check | 5 min |
| **PROJECT_INDEX.md** | This file | Navigation map | 5 min |

**Total Documentation**: ~53 KB of professional guides

---

## ✨ What This Structure Provides

✅ **Professional Organization** - Industry standard  
✅ **Scalability** - Easy to extend  
✅ **Maintainability** - Clear organization  
✅ **Testability** - Built for testing  
✅ **Type Safety** - Type hints throughout  
✅ **Error Handling** - Custom exceptions  
✅ **Logging** - Built-in monitoring  
✅ **Configuration** - Centralized settings  
✅ **Documentation** - Comprehensive guides  
✅ **Production Ready** - Enterprise standards  

---

## 🎓 Learning Path for Beginners

### Day 1: Understanding
1. Read: `QUICKSTART.md` (5 min)
2. Read: `STRUCTURE.md` (10 min)
3. Skim: `INFO.md` (10 min)
4. Run: `python run.py`

### Day 2: Experimentation
1. Read: Full `INFO.md` (30 min)
2. Create: Your first tool in `app/agents/tools/`
3. Write: Unit test in `tests/unit/`

### Day 3: Migration
1. Read: `MIGRATION.md` (15 min)
2. Move: Your existing code
3. Update: All import statements

### Day 4+: Production
1. Write: Integration tests
2. Deploy: To production
3. Monitor: Your application

---

## 🎯 Next Action

👉 **Start here**: Open `QUICKSTART.md` (5 minute read)  
Then: Read `INFO.md` (30 minute reference)  
Finally: Start coding!

---

**Your professional, enterprise-grade project structure is ready!** 🚀

Questions? Check the relevant documentation file above.
