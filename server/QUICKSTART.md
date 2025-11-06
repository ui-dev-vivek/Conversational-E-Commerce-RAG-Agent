# 🚀 Quick Start Guide - New Structure

Your project now has a **professional, company-standard structure**. Here's how to navigate and use it.

---

## 📚 Read These First

1. **`INFO.md`** - Complete documentation (read first!)
2. **`STRUCTURE.md`** - Visual tree & quick reference
3. **`MIGRATION.md`** - How to move your existing code (read if migrating)

---

## 🗂️ Where to Find Things?

### 🔍 I want to...

#### **Add a new chat tool (like "Cancel Order")**
1. Create: `app/agents/tools/order_tools.py`
2. Define class: `CancelOrderTool(BaseTool)`
3. Register in: `app/agents/tools/tool_registry.py`
4. Test in: `tests/unit/test_order_tools.py`

#### **Add a new retriever strategy**
1. Create: `app/rag/retrievers/my_retriever.py`
2. Inherit from: `BaseRetriever`
3. Implement: `retrieve()` method
4. Register in: Vector store factory

#### **Add a new conversation memory backend**
1. Create: `app/memory/chat_history/redis_history.py`
2. Inherit from: `BaseHistory`
3. Use in: Routes via dependency injection

#### **Add a new API endpoint**
1. Create route in: `app/routes/my_feature.py`
2. Include in: `app/main.py` → `app.include_router()`
3. Use dependency injection for LLM, RAG, agents
4. Add tests in: `tests/integration/test_my_feature.py`

#### **Configure LLM (OpenRouter, Anthropic, etc.)**
1. Set env vars in: `.env`
2. Configure in: `app/core/config.py`
3. Create LLM in: `app/services/llm/llm_factory.py`
4. Use in: Routes via dependency injection

#### **Index products to ChromaDB**
1. Run: `python scripts/populate_embeddings.py`
2. Reads from: `data/products.json`
3. Creates: ChromaDB vector store

#### **Initialize database**
1. Run: `python scripts/init_db.py`
2. Creates tables from: `app/models/models.py`
3. Seeds data to: PostgreSQL/SQLite

---

## 📁 Folder Purpose Quick Map

| Folder | Purpose | Example |
|--------|---------|---------|
| `app/core/` | Config, constants, app settings | Environment vars, API keys |
| `app/rag/` | Embeddings, vectors, retrievers | ChromaDB, MiniLM embedder |
| `app/agents/` | Agent tools & execution | Product search tool, agent executor |
| `app/memory/` | Conversation storage | Chat history, context manager |
| `app/services/` | Business logic orchestration | RAG pipeline, LLM service, agent service |
| `app/routes/` | API endpoints | `/api/chat/message`, `/api/products/*` |
| `app/models/` | Database schema | User, Product, Order models |
| `app/schemas/` | Request/response validation | ChatMessageRequest, OrderResponse |
| `app/exceptions/` | Custom errors | RAGException, ToolException |
| `app/validators/` | Input validation | Message validation, query sanitization |
| `app/middlewares/` | HTTP middleware | Error handling, logging |
| `tests/` | Test suite | Unit tests, integration tests |
| `scripts/` | Admin utilities | Init DB, populate embeddings |
| `data/` | Seed data | Products JSON, FAQs, knowledge base |

---

## 🔄 Request Lifecycle

### When user sends: **"Show me red t-shirts"**

```
1. Frontend sends POST /api/chat/message
2. routes/chat.py receives request
3. RoutingChain determines: "needs tools" → agent
4. Agent executor calls: SearchProductsTool
5. Tool queries: app/models (database)
6. LLM generates response with context
7. Response saved to: memory/chat_history
8. Response sent back to frontend
```

### When user asks: **"What's your return policy?"**

```
1. Frontend sends POST /api/chat/message
2. routes/chat.py receives request
3. RoutingChain determines: "needs RAG" → retrieval
4. RAG pipeline:
   - Embed query (embeddings/local_embedder)
   - Search vectorstore (vectorstore/chroma_store)
   - Get top-3 documents (retrievers/similarity_retriever)
5. LLM answers with context
6. Response saved to: memory/chat_history
7. Response sent back to frontend
```

---

## 🎯 Common Tasks

### Task 1: Add new tool
```bash
# 1. Create tool
nano app/agents/tools/new_tool.py

# 2. Define class
class MyNewTool(BaseTool):
    name = "my_tool"
    description = "..."
    
    def run(self, **kwargs):
        pass

# 3. Register
# Update app/agents/tools/tool_registry.py

# 4. Test
pytest tests/unit/test_new_tool.py -v
```

### Task 2: Index products to RAG
```bash
# 1. Place products.json in data/
# 2. Run indexing script
python scripts/populate_embeddings.py

# 3. Verify ChromaDB created
ls -la chroma_data/
```

### Task 3: Add new endpoint
```bash
# 1. Create route
nano app/routes/my_route.py

# 2. Include in main.py
app.include_router(my_router, prefix="/api/my", tags=["my"])

# 3. Test
curl http://localhost:8000/api/my/endpoint
```

### Task 4: Run tests
```bash
# All tests
pytest tests/ -v

# Unit tests only
pytest tests/unit/ -v

# With coverage
pytest tests/ --cov=app --cov-report=html
```

---

## 🔑 Key Files to Understand

### Must-Read Files (in order):
1. **`app/main.py`** - App initialization, routes setup
2. **`app/routes/chat.py`** - Main chat endpoint
3. **`app/agents/chains/agent_executor.py`** - Agent execution
4. **`app/services/rag/rag_pipeline.py`** - RAG orchestration
5. **`app/agents/tools/tool_registry.py`** - All available tools

### Important Modules:
- **`app/core/config.py`** - All configuration
- **`app/models/models.py`** - Database schema
- **`app/services/llm/llm_factory.py`** - LLM creation
- **`app/memory/context_manager.py`** - Context management

---

## 🧪 Testing Structure

```
tests/
├── conftest.py              # Pytest fixtures
├── unit/                    # Individual component tests
│   ├── test_embeddings.py
│   ├── test_retrievers.py
│   ├── test_tools.py
│   └── test_validators.py
│
├── integration/             # Component interaction tests
│   ├── test_rag_pipeline.py
│   ├── test_agent_executor.py
│   └── test_chat_endpoint.py
│
└── fixtures/                # Mock data
    └── mock_data.py
```

### Run tests:
```bash
# All tests
pytest

# Specific test file
pytest tests/unit/test_embeddings.py -v

# Specific test
pytest tests/unit/test_embeddings.py::test_embed_function -v

# With coverage
pytest --cov=app
```

---

## 📋 Configuration (.env)

Create `.env` based on `.env.example`:

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost/ec_chat

# LLM
LLM_PROVIDER=openrouter  # openrouter, anthropic, openai
LLM_API_KEY=your_api_key
LLM_MODEL=gpt-3.5-turbo

# RAG
EMBEDDINGS_MODEL=all-MiniLM-L6-v2
VECTORSTORE_PATH=./chroma_data

# Security
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```

---

## 🚀 Starting the Server

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup database
python scripts/init_db.py

# 3. Index products to RAG
python scripts/populate_embeddings.py

# 4. Start server
python run.py
# or
uvicorn app.main:app --reload

# 5. Visit API docs
# http://localhost:8000/docs
```

---

## 🆘 Troubleshooting

### Import errors?
```bash
# Make sure you're in the right directory
cd server/

# Check __init__.py files exist
find . -type d -exec test -e "{}/__init__.py" \; -print

# Reinstall dependencies
pip install -r requirements.txt
```

### Database connection errors?
```bash
# Check DATABASE_URL in .env
cat .env | grep DATABASE_URL

# Test connection
python -c "from app.config.database import engine; print(engine)"

# Reinitialize
python scripts/init_db.py
```

### LLM API errors?
```bash
# Check .env has correct LLM_API_KEY
cat .env | grep LLM_API_KEY

# Test LLM service
python -c "from app.services.llm import create_llm; llm = create_llm(); print(llm)"
```

---

## 💡 Best Practices

✅ **DO:**
- Put business logic in `services/`
- Use dependency injection from `dependencies/injections.py`
- Write tests for new tools and retrievers
- Use custom exceptions for error handling
- Document complex functions

❌ **DON'T:**
- Put business logic in routes
- Hardcode API keys (use `.env`)
- Create LLMs directly in routes
- Skip input validation
- Commit sensitive data to git

---

## 📚 Next Steps

1. **Read `INFO.md`** for complete documentation
2. **Read `MIGRATION.md`** to move existing code
3. **Create tools** in `app/agents/tools/`
4. **Create tests** in `tests/`
5. **Deploy** with confidence! 🚀

---

## 📞 Quick Reference

| Command | Purpose |
|---------|---------|
| `python run.py` | Start development server |
| `pytest tests/ -v` | Run all tests |
| `python scripts/init_db.py` | Initialize database |
| `python scripts/populate_embeddings.py` | Index to RAG |
| `curl http://localhost:8000/docs` | View API documentation |

---

**Happy coding! Your project is now production-ready! 🎉**
