# Backend Testing Guide - E-Commerce Chat Assistant

## Test Scenarios

### 1. Authentication Tests

#### Register New User
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@test.com",
    "password": "password123",
    "full_name": "New User"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'
```

---

### 2. Product Search Tests

#### Search by Name
```bash
# Search for "kurti"
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","message":"Show me kurti"}'

# Search for "candle"
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","message":"Find candles"}'
```

#### List Categories
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","message":"What categories do you have?"}'
```

---

### 3. Cart Operations Tests

#### View Empty Cart
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","message":"Show my cart"}'
```

#### Add to Cart (via chat)
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","message":"Add Lavender Bliss Candle to cart"}'
```

#### View Cart with Items
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","message":"Show my cart"}'
```

---

### 4. Order Tests

#### Create Order
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","message":"Place order"}'
```

#### List Orders
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","message":"Show my orders"}'
```

---

### 5. RAG Tests (General Questions)

#### FAQ Query
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","message":"What is your return policy?"}'
```

#### Store Info
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","message":"Where is your store located?"}'
```

---

## Direct Database Tests

### Check Products
```bash
# Count products
mysql -u root ecommerce_chat_assistant -e "SELECT COUNT(*) as total FROM products;"

# View sample products
mysql -u root ecommerce_chat_assistant -e "SELECT sku, name, price, category_id FROM products LIMIT 5;"

# Search products
mysql -u root ecommerce_chat_assistant -e "SELECT name, price FROM products WHERE name LIKE '%candle%';"
```

### Check Users
```bash
mysql -u root ecommerce_chat_assistant -e "SELECT id, username, email FROM users;"
```

### Check Cart
```bash
mysql -u root ecommerce_chat_assistant -e "SELECT * FROM cart_items;"
```

---

## Expected Results

### ✅ Working Features
- Authentication (register/login)
- Product search by name
- Category listing
- Cart operations (add, view, remove, clear)
- Order creation and tracking
- RAG for general questions

### 🐛 Known Issues
- Product search case sensitivity (searching "Candles" vs "candles")
- Need to extract product names from natural language queries

---

## Quick Test Script

Run all tests:
```bash
#!/bin/bash

echo "=== Testing Authentication ==="
curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}' | python3 -m json.tool

echo -e "\n=== Testing Categories ==="
curl -s -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","message":"What categories do you have?"}' | python3 -m json.tool

echo -e "\n=== Testing Cart ==="
curl -s -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","message":"Show my cart"}' | python3 -m json.tool

echo -e "\n=== Testing Product Search ==="
curl -s -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","message":"Show me products"}' | python3 -m json.tool
```
