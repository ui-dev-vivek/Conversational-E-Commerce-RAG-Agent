import { useState } from 'react'
import './App.css'
import ChatWidget from './ChatWidget'

const sampleProducts = [
  { id: 1, title: 'Smart LED TV 43" (FHD)', price: '₹24,999', mrp: '₹39,999', rating: 4.3, image: 'https://picsum.photos/id/1069/800/600' },
  { id: 2, title: 'Wireless Headphones', price: '₹1,499', mrp: '₹2,999', rating: 4.1, image: 'https://picsum.photos/id/1027/800/600' },
  { id: 3, title: 'Casual Shoes - Men', price: '₹899', mrp: '₹1,599', rating: 4.0, image: 'https://picsum.photos/id/100/800/600' },
  { id: 4, title: 'Smartphone 8GB/128GB', price: '₹12,999', mrp: '₹16,999', rating: 4.4, image: 'https://picsum.photos/id/1/800/600' },
  { id: 5, title: 'Wrist Watch - Classic', price: '₹2,299', mrp: '₹3,999', rating: 4.2, image: 'https://picsum.photos/id/1025/800/600' },
  { id: 6, title: 'Gaming Keyboard', price: '₹2,999', mrp: '₹4,599', rating: 4.0, image: 'https://picsum.photos/id/1050/800/600' }
]

const categories = [
  { id: 1, title: 'Mobiles', image: 'https://picsum.photos/id/1060/400/300' },
  { id: 2, title: 'Electronics', image: 'https://picsum.photos/id/1057/400/300' },
  { id: 3, title: 'Fashion', image: 'https://picsum.photos/id/1003/400/300' },
  { id: 4, title: 'Home', image: 'https://picsum.photos/id/1016/400/300' },
  { id: 5, title: 'Appliances', image: 'https://picsum.photos/id/1043/400/300' },
  { id: 6, title: 'Beauty', image: 'https://picsum.photos/id/1021/400/300' },
  { id: 7, title: 'Toys', image: 'https://picsum.photos/id/1012/400/300' },
  { id: 8, title: 'Sports', image: 'https://picsum.photos/id/1024/400/300' }
]

function Header() {
  return (
    <header className="fk-header">
      <div className="container">
        <div className="fk-top">
          <div className="fk-logo">Flipkart</div>
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
          <div className="category">Electronics</div>
          <div className="category">Mobiles</div>
          <div className="category">Fashion</div>
          <div className="category">Home</div>
          <div className="category">Appliances</div>
          <div className="category">Beauty</div>
        </div>
      </div>
    </header>
  )
}

function Banner() {
  return (
    <section className="fk-banner">
      <div className="banner-left">
        <h2>Big Savings on Electronics</h2>
        <p>Up to 70% off | Limited time</p>
        <button className="cta">Shop Now</button>
      </div>
      <div className="banner-right">
        <img src="https://picsum.photos/id/1015/1200/500" alt="banner" />
      </div>
    </section>
  )
}

function ProductGrid() {
  return (
    <section className="fk-products">
      <h3>Top Picks for You</h3>
      <div className="grid">
        {sampleProducts.map((p) => (
          <div key={p.id} className="product-card">
            <img src={p.image} alt={p.title} />
            <div className="product-info">
              <div className="product-title">{p.title}</div>
              <div className="product-meta">
                <span className="product-price">{p.price}</span>
                <span className="product-mrp">{p.mrp}</span>
                <span className="product-rating">★ {p.rating}</span>
              </div>
            </div>
            <button className="add-btn">Add to Cart</button>
          </div>
        ))}
      </div>
    </section>
  )
}

function CategoriesGrid() {
  return (
    <section className="fk-categories">
      <h3>Shop by Category</h3>
      <div className="cat-grid">
        {categories.map((c) => (
          <div key={c.id} className="cat-card">
            <img src={c.image} alt={c.title} />
            <div className="cat-title">{c.title}</div>
          </div>
        ))}
      </div>
    </section>
  )
}

function Footer() {
  return (
    <footer className="fk-footer">
      <div className="footer-inner">
        <div className="footer-col">
          <h4>About</h4>
          <p>About Flipkart-like demo</p>
        </div>
        <div className="footer-col">
          <h4>Help</h4>
          <p>Payments | Shipping | Returns</p>
        </div>
        <div className="footer-col">
          <h4>Follow us</h4>
          <p>Twitter / Facebook / Instagram</p>
        </div>
      </div>
      <div className="footer-bottom">© Demo — Flipkart style clone</div>
    </footer>
  )
}

function App() {
  return (
    <div id="app-root">
      <Header />
      <main className="main-content">
        <div className="container">
          <Banner />
          <CategoriesGrid />
          <ProductGrid />
        </div>
      </main>
      <ChatWidget />
      <Footer />
    </div>
  )
}

export default App
