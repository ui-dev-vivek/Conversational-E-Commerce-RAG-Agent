# Quick Test Guide - E-Commerce Chat Assistant

## 🚀 How to Test

### 1. Start Backend
```bash
cd server
python3 run.py
```
✅ Backend should start at `http://localhost:8000`

### 2. Start Frontend
```bash
cd client
npm run dev
```
✅ Frontend should start at `http://localhost:5173`

---

## 🧪 Test Scenarios

### Test 1: Product Search with Cards
**Query**: "Show me kurtis"

**Expected Result**:
- AI responds with product list
- Product cards appear below message
- Each card shows:
  - Product name (bold)
  - Price in ₹
  - "Add to Cart" button
- Cards have hover effects

### Test 2: General FAQ (RAG)
**Query**: "What is your return policy?"

**Expected Result**:
- AI responds with policy information
- No product cards (just text)
- Response formatted with line breaks

### Test 3: Category Listing
**Query**: "What categories do you have?"

**Expected Result**:
- List of categories with product counts
- Formatted text with bullet points (•)
- No product cards

### Test 4: Cart Operations
**Query 1**: "Show my cart"
**Expected**: "Your cart is empty..."

**Query 2**: Click "Add to Cart" on a product
**Expected**: Confirmation message

**Query 3**: "Show my cart" again
**Expected**: Cart items listed

### Test 5: Add to Cart via Button
1. Search for products: "Show me candles"
2. Click "Add to Cart" button on any product card
3. Should auto-send message and get confirmation

---

## ✅ What to Check

### Visual Elements
- [ ] Chat widget opens/closes smoothly
- [ ] Messages have proper avatars (🤖 for AI, 👤 for user)
- [ ] Product cards display correctly
- [ ] Bold text (**text**) renders properly
- [ ] Line breaks work in messages
- [ ] Hover effects on product cards
- [ ] "Add to Cart" button hover effects

### Functionality
- [ ] Product search returns cards
- [ ] FAQ queries return text only
- [ ] Add to cart button works
- [ ] Message history persists
- [ ] Typing indicator shows
- [ ] Auto-scroll to latest message

### Responsive Design
- [ ] Works on desktop
- [ ] Works on mobile (product cards stack vertically)
- [ ] Chat widget fills screen on mobile

---

## 🐛 Common Issues

### Issue: "Command 'python' not found"
**Solution**: Use `python3` instead of `python`

### Issue: Frontend can't connect to backend
**Solution**: 
1. Check backend is running on port 8000
2. Check CORS settings in `server/app/main.py`
3. Clear browser cache

### Issue: Product cards not showing
**Solution**:
1. Check browser console for errors
2. Verify API response has product data
3. Check product regex pattern in `parseProductsFromResponse`

---

## 📸 Expected Screenshots

### Product Search Result
```
AI: I found 1 products for you:

┌─────────────────────────────────────┐
│ Elegant Cotton Kurti        ₹1,499  │
│                    [Add to Cart]    │
└─────────────────────────────────────┘

Would you like to add any of these to your cart?
```

### Cart View
```
AI: Your cart is empty. Browse our products and add items you like!
```

---

## 🎯 Success Criteria

✅ All test scenarios pass
✅ Product cards display correctly
✅ Add to cart functionality works
✅ RAG queries work without cards
✅ UI is responsive and smooth
✅ No console errors

---

## 📞 Need Help?

Check the logs:
- **Backend**: Terminal running `python3 run.py`
- **Frontend**: Browser console (F12)
- **Network**: Browser DevTools → Network tab
