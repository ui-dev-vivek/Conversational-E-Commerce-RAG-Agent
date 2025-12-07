import { useState } from 'react'
import './App.css'
import ChatWidget, { AuthProvider } from './ChatWidget'

// Fetch real products from API
const fetchProducts = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/chat/message', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: 'guest',
        message: 'Show me all products'
      })
    })
    const data = await response.json()
    return data.products || []
  } catch (error) {
    console.error('Error fetching products:', error)
    return []
  }
}

function App() {
  const [chatOpen, setChatOpen] = useState(false)
  const [chatMessage, setChatMessage] = useState('')

  const handleAddToCart = (productName) => {
    setChatMessage(`Add ${productName} to cart`)
    setChatOpen(true)
  }

  return (
    <AuthProvider>
      <div id="app-root" className="main-content">
        <Header />
        <Banner />
        <ProductSection onAddToCart={handleAddToCart} />
        <Footer />
        <ChatWidget autoOpen={chatOpen} initialMessage={chatMessage} />
      </div>
    </AuthProvider>
  )
}

function Header() {
  return (
    <header className="fk-header">
      <div className="container">
        <div className="fk-top">
          <div className="fk-logo">AJ Creations</div>
          <div className="fk-search">
            <input placeholder="Search for products, brands and more" />
            <button>Search</button>
          </div>
          <nav className="fk-nav">
            <button className="nav-btn">Login</button>
            <button className="nav-btn">More</button>
            <button className="nav-btn cart">Cart</button>
          </nav>
        </div>
        <div className="fk-category-strip">
          <div className="category">Women's Clothing</div>
          <div className="category">Cosmetics</div>
          <div className="category">Candles</div>
          <div className="category">Soaps</div>
          <div className="category">Home Decor</div>
        </div>
      </div>
    </header>
  )
}

function Banner() {
  return (
    <section className="fk-banner">
      <div className="banner-left">
        <h2>Handcrafted with Love ❤️</h2>
        <p>Authentic Indian Handicrafts | Free Shipping</p>
        <button className="cta">Shop Now</button>
      </div>
      <div className="banner-right">
        <img src="https://picsum.photos/id/1015/800/400" alt="Banner" />
      </div>
    </section>
  )
}

function ProductSection({ onAddToCart }) {
  // Sample products from our database categories
  const products = [
    { id: 1, title: 'Elegant Cotton Kurti', price: '₹1,499', category: 'Clothing', image: 'https://picsum.photos/id/1011/400/400' },
    { id: 2, title: 'Lavender Bliss Candle', price: '₹499', category: 'Candles', image: 'https://picsum.photos/id/1012/400/400' },
    { id: 3, title: 'Natural Face Cream', price: '₹899', category: 'Cosmetics', image: 'https://picsum.photos/id/1013/400/400' },
    { id: 4, title: 'Handmade Soap Set', price: '₹599', category: 'Soaps', image: 'https://picsum.photos/id/1014/400/400' },
    { id: 5, title: 'Floral Print Saree', price: '₹2,999', category: 'Clothing', image: 'https://picsum.photos/id/1015/400/400' },
    { id: 6, title: 'Decorative Glass Vase', price: '₹799', category: 'Decor', image: 'https://picsum.photos/id/1016/400/400' },
  ]

  return (
    <section className="product-section">
      <h2 className="section-title">Featured Products</h2>
      <div className="product-grid">
        {products.map(product => (
          <div key={product.id} className="product-card-home">
            <img src={product.image} alt={product.title} />
            <div className="product-details">
              <h3>{product.title}</h3>
              <p className="category">{product.category}</p>
              <div className="price-row">
                <span className="price">{product.price}</span>
                <button
                  className="add-to-cart-btn"
                  onClick={() => onAddToCart(product.title)}
                >
                  Add to Cart
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}

function Footer() {
  return (
    <footer className="fk-footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-col">
            <h4>About</h4>
            <p>AJ Creations - Authentic Indian Handicrafts</p>
          </div>
          <div className="footer-col">
            <h4>Contact</h4>
            <p>Email: support@ajcreations.in</p>
            <p>Phone: +91-7619876249</p>
          </div>
          <div className="footer-col">
            <h4>Follow Us</h4>
            <p>Instagram | Facebook | Twitter</p>
          </div>
        </div>
        <div className="footer-bottom">
          <p>© 2024 AJ Creations. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}

export default App
