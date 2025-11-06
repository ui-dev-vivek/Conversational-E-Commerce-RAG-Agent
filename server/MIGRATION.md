# 📋 Migration Guide - Old to New Structure

This guide helps you move your existing files to the new company-standard structure.

---

## ✅ Checklist: File Reorganization

### 1. Configuration Files
- [ ] Move `app/config/settings.py` → `app/core/config.py`
  - Consolidate with any existing Pydantic Settings
  - Update imports throughout the project

- [ ] Delete `app/config/` folder (after migration)
  - Keep `app/config/database.py` temporarily for backward compatibility

### 2. RAG Components
- [ ] Move `app/rag/embedder.py` → `app/rag/embeddings/local_embedder.py`
  - Implement the `base_embedder.py` interface

- [ ] Move `app/rag/retriever.py` → `app/rag/retrievers/similarity_retriever.py`
  - Implement the `base_retriever.py` interface

- [ ] If you have existing tools:
  - Move `app/rag/agent_tools.py` → `app/agents/tools/`
  - Split into: `product_tools.py`, `order_tools.py`, `cart_tools.py`, etc.

### 3. Services Layer
- [ ] Refactor `app/services/llm.py` → `app/services/llm/base_llm.py`
  - Create `app/services/llm/llm_factory.py`

- [ ] Rename `app/services/Chain.py` → `app/services/rag/rag_pipeline.py`
  - This is your RAG orchestration

- [ ] Create `app/services/agent/agent_service.py`
  - High-level agent execution wrapper

### 4. Database & Models
- [ ] Keep `app/models/models.py` as is
  - Already using SQLAlchemy ORM (✓ Good!)

- [ ] Keep `app/config/database.py` as is for now
  - Later refactor DB setup to `app/core/config.py`

### 5. Routes
- [ ] Keep `app/routes/auth.py`, `orders.py`, `products.py` as is
  - Update imports to reflect new structure

- [ ] Keep `app/routes/chat.py` but update to use new services:
  ```python
  from app.services.agent import AgentService
  from app.services.rag import RAGPipeline
  from app.memory.chat_history import DatabaseHistory
  ```

### 6. Utils & Auth
- [ ] Keep `app/utils/auth.py` as is
  - Rename folder to `app/utils/` (already done)

### 7. New Additions
- [ ] Create `app/exceptions/base_exceptions.py`
- [ ] Create `app/validators/input_validators.py`
- [ ] Create `app/constants/messages.py`
- [ ] Create `app/constants/enums.py`
- [ ] Create `app/middlewares/error_handler.py`
- [ ] Create `app/middlewares/logging_middleware.py`
- [ ] Create `app/logging_config/logger.py`
- [ ] Create `app/dependencies/injections.py`

### 8. Testing
- [ ] Move any existing tests to `tests/unit/` or `tests/integration/`
- [ ] Create `tests/conftest.py` with shared fixtures
- [ ] Create `tests/fixtures/mock_data.py` with test data

### 9. Scripts
- [ ] Move `app/create_tables.py` → `scripts/init_db.py`
- [ ] Create `scripts/populate_embeddings.py` to index RAG data

---

## 🔄 Import Updates

After reorganization, update imports everywhere:

### Before:
```python
from app.config.settings import Settings
from app.rag.embedder import Embedder
from app.rag.retriever import Retriever
from app.services.llm import Llm
from app.rag.agent_tools import ProductSearchTool
```

### After:
```python
from app.core.config import Settings
from app.rag.embeddings.local_embedder import LocalEmbedder
from app.rag.retrievers.similarity_retriever import SimilarityRetriever
from app.services.llm.llm_factory import create_llm
from app.agents.tools.product_tools import SearchProductsTool
from app.services.agent import AgentService
```

---

## 📊 File Mapping

| Old Path | New Path | Notes |
|----------|----------|-------|
| `app/config/settings.py` | `app/core/config.py` | ⭐ Consolidate here |
| `app/rag/embedder.py` | `app/rag/embeddings/local_embedder.py` | Implement interface |
| `app/rag/retriever.py` | `app/rag/retrievers/similarity_retriever.py` | Implement interface |
| `app/rag/agent_tools.py` | `app/agents/tools/*.py` | Split by domain |
| `app/services/llm.py` | `app/services/llm/base_llm.py` | Create factory |
| `app/services/Chain.py` | `app/services/rag/rag_pipeline.py` | Rename |
| `app/create_tables.py` | `scripts/init_db.py` | Move to scripts |
| `app/config/database.py` | `app/core/config.py` | Consolidate later |

---

## 🎯 Priority Order

### Phase 1: High Priority (Day 1)
1. Create `app/core/config.py` with all settings
2. Reorganize RAG components (embedder, retriever, tools)
3. Update imports in `app/routes/chat.py`
4. Update imports in `app/main.py`

### Phase 2: Medium Priority (Day 2)
1. Create services layer (LLM, RAG, Agent)
2. Create exception handling & validators
3. Create dependency injection
4. Add middleware

### Phase 3: Polish (Day 3+)
1. Create tests
2. Create migration scripts
3. Add documentation

---

## 🔗 Example: Move Embedder

### Before:
```
app/rag/embedder.py
├── class Embedder
```

### After:
```
app/rag/embeddings/local_embedder.py
├── class LocalEmbedder(BaseEmbedder)

app/rag/embeddings/base_embedder.py
├── class BaseEmbedder (ABC)
```

### Code:
```python
# app/rag/embeddings/base_embedder.py
from abc import ABC, abstractmethod

class BaseEmbedder(ABC):
    @abstractmethod
    def embed(self, text: str) -> List[float]:
        pass
    
    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        pass

# app/rag/embeddings/local_embedder.py
from .base_embedder import BaseEmbedder
from sentence_transformers import SentenceTransformer

class LocalEmbedder(BaseEmbedder):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    def embed(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts).tolist()
```

---

## 🔗 Example: Move Tool

### Before:
```
app/rag/agent_tools.py
├── SearchProductsTool
├── GetOrderStatusTool
├── AddToCartTool
```

### After:
```
app/agents/tools/product_tools.py
├── SearchProductsTool

app/agents/tools/order_tools.py
├── GetOrderStatusTool

app/agents/tools/cart_tools.py
├── AddToCartTool

app/agents/tools/tool_registry.py
├── get_all_tools() -> List[Tool]
```

### Code:
```python
# app/agents/tools/base_tool.py
from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTool(ABC):
    name: str
    description: str
    
    @abstractmethod
    def run(self, **kwargs) -> str:
        pass

# app/agents/tools/product_tools.py
from .base_tool import BaseTool

class SearchProductsTool(BaseTool):
    name = "search_products"
    description = "Search for products by name, category, price"
    
    def run(self, query: str, category: str = None, max_price: float = None) -> str:
        # Implementation
        pass

# app/agents/tools/tool_registry.py
from .product_tools import SearchProductsTool
from .order_tools import GetOrderStatusTool
# ... import all tools

def get_all_tools() -> List[BaseTool]:
    return [
        SearchProductsTool(),
        GetOrderStatusTool(),
        # ... all other tools
    ]
```

---

## 🧪 Testing After Migration

Run these commands to verify:

```bash
# Check imports
python -m py_compile app/main.py
python -m py_compile app/routes/chat.py

# Run tests
pytest tests/unit/ -v
pytest tests/integration/ -v

# Start server
uvicorn app.main:app --reload
```

---

## ✨ Summary

After migration, you'll have:

✅ **Professional structure** - Industry standard
✅ **Scalability** - Easy to add new tools, retrievers, prompts
✅ **Testability** - Clear separation of concerns
✅ **Maintainability** - Well-organized, documented
✅ **Type safety** - Better IDE support with factories & interfaces
✅ **Extensibility** - Factory patterns for easy additions

🎉 **Your project is now enterprise-ready!**
