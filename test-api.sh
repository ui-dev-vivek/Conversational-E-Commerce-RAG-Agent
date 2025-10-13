#!/bin/bash

# Quick test script for the E-Commerce Chat API

echo "🧪 Testing E-Commerce Chat API"
echo "================================"
echo ""

# Test if backend is running
echo "1️⃣ Checking if backend is running on port 8000..."
if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
    echo "✅ Backend is running!"
else
    echo "❌ Backend is NOT running on port 8000"
    echo "   Start it with: cd server && python3 run.py"
    exit 1
fi

echo ""
echo "2️⃣ Testing /api/chat/message endpoint..."

# Test the chat endpoint
RESPONSE=$(curl -s -X POST \
  'http://127.0.0.1:8000/api/chat/message' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"message": "Hello from test script!"}')

echo "Response: $RESPONSE"

if echo "$RESPONSE" | grep -q "reply"; then
    echo "✅ Chat endpoint is working!"
else
    echo "❌ Chat endpoint returned unexpected response"
    exit 1
fi

echo ""
echo "3️⃣ All tests passed! 🎉"
echo ""
echo "📌 Next steps:"
echo "   1. Open http://localhost:5174 in your browser"
echo "   2. Click the chat button (💬 Chat)"
echo "   3. Type a message and press Enter"
echo "   4. Check browser console (F12) for detailed logs"
