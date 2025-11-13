# 📊 Server Project Structure - Company Standard

This document explains the complete folder and file structure of the FastAPI + LangChain RAG backend with professional standards.

---

## 📁 Directory Structure Overview

```
server/
├── app/                              # Main application package
│   ├── __init__.py                  # Package initialization
│   ├── core/                        # ⭐ CORE CONFIGS & SETUP
│   │   ├── __init__.py
│   │   ├── config.py                # Pydantic Settings for env vars, DB, LLM, RAG configs
│   │   └── constants.py             # Global constants and app-wide settings
        |    llmbase.py                # Base LLM class with factory pattern
│   │
│   ├── rag/                         # ⭐ RAG PIPELINE (Retrieval-Augmented Generation)
│   │   ├── __init__.py
│   │   ├── embeddings/              # Text embedding models
│   │   │   ├── __init__.py
│   │   │   ├── embedding_factory.py # Factory to create embedders (local, OpenAI, etc.)
│   │   │   └── local_embedder.py    # sentence-transformers wrapper (MiniLM-L6-v2)
│   │   │
│   │   ├── vectorstore/             # Vector databases (ChromaDB, Pinecone, etc.)
│   │   │   ├── __init__.py
│   │   │   ├── chroma_store.py      # ChromaDB implementation
│   │   │   └── store_factory.py     # Factory to create different vector stores
│   │   │
│   │   ├── retrievers/              # Document retrieval strategies
│   │   │   ├── __init__.py
│   │   │   ├── base_retriever.py    # Abstract base class
│   │   │   ├── similarity_retriever.py  # Semantic similarity search
│   │   │   └── hybrid_retriever.py  # Hybrid BM25 + semantic search
│   │   │
│   │   └── prompts/                 # System prompts & templates
│   │       ├── __init__.py
│   │       ├── system_prompts.py    # Role-based system messages
│   │       └── prompt_templates.py  # LangChain PromptTemplates
│   │
│   ├── agents/                      # ⭐ AGENT ORCHESTRATION (LangGraph)
│   │   ├── __init__.py
│   │   ├── tools/                   # ⚙️ TOOLS FOR AGENTS
│   │   │   ├── __init__.py
│   │   │   ├── base_tool.py         # Abstract tool interface
│   │   │   ├── product_tools.py     # SearchProducts, GetProductDetails, FilterProducts
│   │   │   ├── order_tools.py       # GetOrderStatus, ListOrders, TrackOrder
│   │   │   ├── cart_tools.py        # AddToCart, RemoveFromCart, Checkout
│   │   │   ├── user_tools.py        # GetProfile, UpdateAddress, GetWishlist
│   │   │   ├── currency_tool.py     # ConvertCurrency, FormatPrice
│   │   │   └── tool_registry.py     # Central registry of all available tools
│   │   │
│   │   └── chains/                  # 🔗 CHAINS & EXECUTORS
│   │       ├── __init__.py
│   │       ├── rag_chain.py         # RAG retrieval chain
│   │       ├── agent_executor.py    # LangGraph agent state machine
│   │       └── routing_chain.py     # Intent routing (agent vs RAG vs LLM)
│   │
│   ├── memory/                      # 💾 CONVERSATION MEMORY
│   │   ├── __init__.py
│   │   ├── chat_history/            # Chat history storage backends
│   │   │   ├── __init__.py
│   │   │   ├── base_history.py      # Abstract history interface
│   │   │   ├── database_history.py  # SQL-backed persistence
│   │   │   └── memory_history.py    # Fast in-memory with Redis option
│   │   └── context_manager.py       # Manages context window & summarization
│   │
│   ├── services/                    # 🔧 BUSINESS LOGIC LAYER
│   │   ├── __init__.py
│   │   ├── llm/                     # LLM Management
│   │   │   ├── __init__.py
│   │   │   ├── base_llm.py          # Abstract LLM interface
│   │   │   └── llm_factory.py       # Factory for LangChain LLMs
│   │   │
│   │   ├── rag/                     # RAG Service Orchestration
│   │   │   ├── __init__.py
│   │   │   ├── rag_pipeline.py      # Complete RAG ingestion & retrieval
│   │   │   └── document_processor.py # Document chunking & cleaning
│   │   │
│   │   └── agent/                   # Agent Service Orchestration
│   │       ├── __init__.py
│   │       └── agent_service.py     # High-level agent execution
│   │
│   ├── routes/                      # 📡 API ENDPOINTS
│   │   ├── __init__.py
│   │   ├── auth.py                  # POST /api/auth/login, /register
│   │   ├── products.py              # GET /api/products/{id}, /search
│   │   ├── orders.py                # GET /api/orders, POST /orders
│   │   └── chat.py                  # POST /api/chat/message (main chat endpoint)
│   │
│   ├── models/                      # 🗄️ DATABASE MODELS (SQLAlchemy ORM)
│   │   ├── __init__.py
│   │   └── models.py                # User, Product, Order, OrderItem, Address, Category
│   │
│   ├── schemas/                     # 📋 REQUEST/RESPONSE SCHEMAS (Pydantic)
│   │   ├── __init__.py
│   │   └── schemas.py               # ChatMessageRequest, ProductResponse, OrderSchema
│   │
│   ├── config/                      # 🗝️ DATABASE & CONNECTION CONFIG
│   │   ├── __init__.py
│   │   ├── database.py              # SQLAlchemy engine, session factory, Base model
│   │   └── settings.py              # Environment variables (DEPRECATED - move to core/config.py)
│   │
│   ├── utils/                       # 🛠️ UTILITY FUNCTIONS
│   │   ├── __init__.py
│   │   └── auth.py                  # JWT token generation, password hashing
│   │
│   ├── exceptions/                  # ⚠️ CUSTOM EXCEPTIONS
│   │   ├── __init__.py
│   │   └── base_exceptions.py       # RAGException, AgentException, ToolException, etc.
│   │
│   ├── validators/                  # ✅ INPUT VALIDATION
│   │   ├── __init__.py
│   │   └── input_validators.py      # Validate messages, queries, parameters
│   │
│   ├── constants/                   # 📌 APPLICATION CONSTANTS
│   │   ├── __init__.py
│   │   ├── messages.py              # Error messages, success messages
│   │   └── enums.py                 # OrderStatus, UserRole, ChatState enums
│   │
│   ├── middlewares/                 # 🔄 FASTAPI MIDDLEWARES
│   │   ├── __init__.py
│   │   ├── error_handler.py         # Global exception handling
│   │   └── logging_middleware.py    # Request/response logging
│   │
│   ├── logging_config/              # 📝 LOGGING SETUP
│   │   ├── __init__.py
│   │   └── logger.py                # Structured logging configuration
│   │
│   ├── dependencies/                # 🔗 DEPENDENCY INJECTION (FastAPI depends)
│   │   ├── __init__.py
│   │   └── injections.py            # DB session, LLM, RAG, agent service providers
│   │
│   └── main.py                      # 🚀 FastAPI app creation & startup logic
│
├── tests/                           # ✔️ TEST SUITE
│   ├── conftest.py                  # Pytest configuration & shared fixtures
│   ├── unit/                        # Unit tests for individual components
│   │   └── __init__.py
│   ├── integration/                 # Integration tests for component interactions
│   │   └── __init__.py
│   └── fixtures/                    # Test data & mocks
│       ├── __init__.py
│       └── mock_data.py             # Sample products, users, orders
│
├── migrations/                      # 🔄 DATABASE MIGRATIONS
│   └── README.md                    # Alembic migration version control
│
├── scripts/                         # 🎯 UTILITY SCRIPTS
│   ├── README.md
│   ├── init_db.py                   # Initialize database tables
│   └── populate_embeddings.py       # Index products to ChromaDB
│
├── data/                            # 📂 SEED DATA & KNOWLEDGE BASE
│   ├── README.md
│   ├── products.json                # (to create) Product catalog for RAG
│   ├── faqs.json                    # (to create) FAQ data for retrieval
│   └── knowledge_base/              # (to create) Documentation & guides
│
├── logs/                            # 📋 APPLICATION LOGS
│   ├── README.md
│   ├── app.log                      # (generated) Application logs
│   └── error.log                    # (generated) Error logs
│
├── run.py                           # Entry point: uvicorn app.main:app --reload
├── requirements.txt                 # Python dependencies
├── .env                             # (git-ignored) Environment variables
├── .env.example                     # Template for .env
└── INFO.md                          # This file - Project documentation
```

---

## 🎯 Folder & File Purposes

### 1️⃣ **`app/core/`** - Core Application Configuration

| File           | Purpose                                                                                                                                                             |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `config.py`    | **Main configuration using Pydantic Settings** - Loads all env vars (API keys, DB URLs, LLM settings, RAG parameters). Use this instead of `app/config/settings.py` |
| `constants.py` | Global constants: API versions, max tokens, chunk sizes, timeouts                                                                                                   |

### 2️⃣ **`app/rag/`** - RAG Pipeline Components

| Folder         | Purpose                                                                   |
| -------------- | ------------------------------------------------------------------------- |
| `embeddings/`  | Text embedding models - wraps sentence-transformers or OpenAI embeddings  |
| `vectorstore/` | Vector database (ChromaDB) - stores product embeddings for retrieval      |
| `retrievers/`  | Document retrieval strategies - semantic similarity, hybrid BM25+semantic |
| `prompts/`     | System prompts & instruction templates for LLM                            |

**Flow**: Raw text → Embeddings → VectorStore → Retriever → Context for LLM

### 3️⃣ **`app/agents/`** - Agent Orchestration (LangGraph)

| Folder    | Purpose                                                                 |
| --------- | ----------------------------------------------------------------------- |
| `tools/`  | **All tools for agents** (SearchProductsTool, GetOrderStatusTool, etc.) |
| `chains/` | Agent executor, RAG chain, and routing logic                            |

**Key files**:

- `tools/product_tools.py` → Search & filter products
- `tools/order_tools.py` → Get order status, history
- `tools/cart_tools.py` → Add to cart, checkout
- `tools/tool_registry.py` → Central registry of all available tools
- `chains/agent_executor.py` → Main LangGraph agent state machine
- `chains/routing_chain.py` → Route user query to agent/RAG/simple LLM

### 4️⃣ **`app/memory/`** - Conversation Memory Management

| File                               | Purpose                                                      |
| ---------------------------------- | ------------------------------------------------------------ |
| `chat_history/database_history.py` | **Persistent storage** - Save conversations to database      |
| `chat_history/memory_history.py`   | **Fast in-memory** - Session-level conversations             |
| `context_manager.py`               | Manages context window, summarization for long conversations |

### 5️⃣ **`app/services/`** - Business Logic Layer

| Folder   | Purpose                                                               |
| -------- | --------------------------------------------------------------------- |
| `llm/`   | LLM initialization & management (OpenRouter, Anthropic, local)        |
| `rag/`   | High-level RAG orchestration - document ingestion, retrieval pipeline |
| `agent/` | High-level agent orchestration - tool execution, state management     |

**These are "orchestrator" services that tie RAG + agents + memory together**

### 6️⃣ **`app/routes/`** - FastAPI Endpoints

| File          | Endpoints                       | Purpose                             |
| ------------- | ------------------------------- | ----------------------------------- |
| `auth.py`     | `/api/auth/login`, `/register`  | User authentication                 |
| `products.py` | `/api/products/{id}`, `/search` | Product listing & search            |
| `orders.py`   | `/api/orders`, `/orders/{id}`   | Order management                    |
| `chat.py`     | **`POST /api/chat/message`**    | Main chat endpoint - uses agent/RAG |

### 7️⃣ **`app/models/`** - Database Models

| Models               | Purpose                       |
| -------------------- | ----------------------------- |
| `User`               | User accounts, authentication |
| `Product`            | E-commerce products catalog   |
| `Order`, `OrderItem` | Orders and line items         |
| `Category`           | Product categories            |
| `Address`            | User shipping addresses       |

### 8️⃣ **`app/schemas/`** - Pydantic Request/Response Schemas

Define request bodies & responses:

```python
class ChatMessageRequest(BaseModel):
    user_id: str
    message: str

class ChatMessageResponse(BaseModel):
    reply: str
    sources: List[Document]
```

### 9️⃣ **`app/exceptions/`** - Custom Exceptions

Define custom errors:

- `RAGException` - Retrieval or embedding errors
- `AgentException` - Tool execution or agent errors
- `ToolException` - Tool not found, execution failed
- `ValidationException` - Input validation failed

### 🔟 **`app/middlewares/`** - FastAPI Middleware

- `error_handler.py` - Global exception catching
- `logging_middleware.py` - Log all API calls

### 1️⃣1️⃣ **`app/constants/`** - Global Constants

- `messages.py` - Error messages, status codes
- `enums.py` - OrderStatus, UserRole, ChatState enums

### 1️⃣2️⃣ **`app/validators/`** - Input Validation

Custom validators for:

- Message length & content
- Query sanitization
- Parameter validation

### 1️⃣3️⃣ **`app/dependencies/`** - Dependency Injection

FastAPI dependencies that provide:

- Database sessions
- LLM instances
- RAG pipeline
- Agent service

### 1️⃣4️⃣ **`tests/`** - Test Suite

```
tests/
├── unit/           # Test individual components (retrievers, tools, etc.)
├── integration/    # Test component interactions (RAG pipeline, agent)
└── fixtures/       # Mock data for testing
```

### 1️⃣5️⃣ **`scripts/`** - Utility Scripts

- `init_db.py` - Create database tables & seed data
- `populate_embeddings.py` - Index products to ChromaDB for RAG

### 1️⃣6️⃣ **`data/`** - Seed Data

Store:

- Product catalog JSON
- FAQ documents
- Knowledge base files
- Test data

### 1️⃣7️⃣ **`logs/`** - Application Logs

- `app.log` - General logs
- `error.log` - Error traces

---

## 🔄 Request Flow Example

**User sends**: `"Show me red laptops under ₹50,000"`

```
ChatWidget (Frontend)
    ↓
POST /api/chat/message {user_id, message}
    ↓
chat.py Router → chat_message endpoint
    ↓
RoutingChain → Intent: "product_search" → Needs Agent
    ↓
Agent Executor (LangGraph)
    ├── Call SearchProductsTool (with filters: color=red, type=laptop, price<50000)
    ├── Tool retrieves from database
    └── Return results to LLM
    ↓
LLM generates: "Found 3 red laptops under ₹50,000: ..."
    ↓
ChatMessageResponse {reply, sources}
    ↓
Frontend displays response
```

---

## 📊 RAG Flow Example

**User sends**: `"What's your return policy?"`

```
ChatWidget (Frontend)
    ↓
POST /api/chat/message {user_id, message}
    ↓
RoutingChain → Intent: "faq_lookup" → Needs RAG
    ↓
RAG Pipeline:
    1. Embed query: "What's your return policy?"
    2. Search VectorStore (ChromaDB) for similar documents
    3. Retrieve top-3 FAQ documents
    4. Rank by relevance
    ↓
LLM (with context): "Based on our FAQ, our return policy is..."
    ↓
ChatMessageResponse {reply, sources: [doc1, doc2, doc3]}
    ↓
Frontend displays response + sources
```

---

## ⚙️ How to Use This Structure

### **Adding a New Tool**

1. Create `app/agents/tools/my_tool.py` (inherit from `base_tool.py`)
2. Register in `app/agents/tools/tool_registry.py`
3. Use in `app/agents/chains/agent_executor.py`

### **Adding a New Endpoint**

1. Create `app/routes/my_feature.py`
2. Include router in `app/main.py`
3. Use dependency injection for LLM, RAG, agent services

### **Adding a New Retriever Strategy**

1. Create `app/rag/retrievers/my_retriever.py` (inherit from `base_retriever.py`)
2. Register in `app/rag/vectorstore/store_factory.py`
3. Use in RAG pipeline

### **Adding a New Memory Backend**

1. Create `app/memory/chat_history/my_history.py` (inherit from `base_history.py`)
2. Use in routes for persistence

---

## 🎓 Best Practices

✅ **DO**:

- Keep business logic in `services/`
- Keep API logic in `routes/`
- Use dependency injection for services
- Create factories for complex objects (LLMs, tools, etc.)
- Write unit tests for tools and retrievers
- Use custom exceptions for error handling
- Store configurations in `core/config.py`

❌ **DON'T**:

- Put business logic in routes
- Hardcode API keys (use `.env`)
- Create LLMs directly in routes (use factories)
- Mix RAG, agents, and memory concerns
- Skip input validation

---

## 📝 Summary Table

| Folder          | Responsibility                 | Key Pattern        |
| --------------- | ------------------------------ | ------------------ |
| `core/`         | Global config & constants      | Pydantic Settings  |
| `rag/`          | Embeddings, retrieval, prompts | Pipeline pattern   |
| `agents/`       | Tool definitions & execution   | Factory + Registry |
| `memory/`       | Conversation storage           | Adapter pattern    |
| `services/`     | Business logic orchestration   | Service layer      |
| `routes/`       | API endpoints                  | FastAPI routers    |
| `models/`       | Database schema                | SQLAlchemy ORM     |
| `schemas/`      | Data validation                | Pydantic models    |
| `exceptions/`   | Error handling                 | Custom exceptions  |
| `validators/`   | Input validation               | Custom validators  |
| `middlewares/`  | Cross-cutting concerns         | Middleware pattern |
| `dependencies/` | Dependency injection           | DI pattern         |
| `tests/`        | Quality assurance              | Pytest             |
| `scripts/`      | Admin utilities                | Click CLI          |

---

## 🚀 Next Steps

1. **Move existing code**:

   - Move `app/config/settings.py` → `app/core/config.py`
   - Move `app/rag/embedder.py` → `app/rag/embeddings/local_embedder.py`
   - Move `app/rag/retriever.py` → `app/rag/retrievers/similarity_retriever.py`
   - Consolidate tools into `app/agents/tools/`

2. **Implement missing layers**:

   - `app/services/llm/llm_factory.py` - Create LLM instances
   - `app/services/rag/rag_pipeline.py` - Orchestrate RAG
   - `app/services/agent/agent_service.py` - Orchestrate agents

3. **Add middleware & error handling**:

   - Global error handler in `app/middlewares/`
   - Custom exceptions in `app/exceptions/`

4. **Complete CI/CD setup**:
   - Add tests in `tests/unit/` and `tests/integration/`
   - Configure pytest in `tests/conftest.py`
