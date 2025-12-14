import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import './App.css';
import Products from './pages/Products';
import Cart from './pages/Cart';
import Auth from './pages/Auth';
import Checkout from './pages/Checkout';
import apiService from './api/apiService';
import ChatWidget, { AuthProvider } from './ChatWidget';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="app">
          <Header />
          <main className="main-content">
            <Routes>

              <Route path="/" element={<Home />} />
              <Route path="/products" element={<Products />} />
              <Route path="/cart" element={<Cart />} />
              <Route path="/login" element={<Auth />} />
              <Route path="/checkout" element={<Checkout />} />
            </Routes>
          </main>
          <Footer />
          <ChatWidget />
        </div>
      </Router>
    </AuthProvider>
  );
}

function Header() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const userData = await apiService.getCurrentUser();
        setUser(userData);
        setIsLoggedIn(true);
      } catch (err) {
        localStorage.removeItem('token');
        setIsLoggedIn(false);
      }
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    apiService.clearToken();
    setIsLoggedIn(false);
    setUser(null);
    navigate('/');
  };

  return (
    <header className="fk-header">
      <div className="container">
        <div className="fk-top">
          <Link to="/" className="fk-logo">AJ Creations</Link>
          <nav className="fk-nav">
            <Link to="/products" className="nav-btn">Products</Link>
            {isLoggedIn ? (
              <>
                <span className="user-name">Hi, {user?.username || 'User'}</span>
                <Link to="/cart" className="nav-btn cart">🛒 Cart</Link>
                <button onClick={handleLogout} className="nav-btn">Logout</button>
              </>
            ) : (
              <Link to="/login" className="nav-btn">Login</Link>
            )}
          </nav>
        </div>
      </div>
    </header>
  );
}

function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-page">
      <section className="hero-banner">
        <div className="hero-content">
          <h1>Handcrafted with Love ❤️</h1>
          <p className="hero-subtitle">Authentic Indian Handicrafts</p>
          <p className="hero-description">
            Discover unique, handmade products crafted by skilled artisans.
            From traditional clothing to natural cosmetics, candles, soaps, and home decor.
          </p>
          <button className="cta-btn" onClick={() => navigate('/products')}>
            Shop Now
          </button>
        </div>
        <div className="hero-image">
          <img src="https://placehold.co/800x600/6c5ce7/ffffff?text=Handcrafted+Collection" alt="Handcrafted Products" />
        </div>
      </section>

      <section className="features">
        <div className="feature-card">
          <div className="feature-icon">🎨</div>
          <h3>Handcrafted</h3>
          <p>Every product is made with care by skilled artisans</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon">🌿</div>
          <h3>Natural</h3>
          <p>Organic and eco-friendly materials</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon">🚚</div>
          <h3>Free Shipping</h3>
          <p>On all orders across India</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon">💯</div>
          <h3>Authentic</h3>
          <p>100% genuine Indian handicrafts</p>
        </div>
      </section>

      <section className="categories-preview">
        <h2>Shop by Category</h2>
        <div className="category-grid">
          {["Women's Clothing", "Cosmetics", "Candles", "Soaps", "Home Decor"].map(cat => (
            <div key={cat} className="category-card" onClick={() => navigate('/products')}>
              <img src={`https://placehold.co/300x300/a29bfe/ffffff?text=${cat.replace(' ', '+')}`} alt={cat} />
              <h3>{cat}</h3>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

function Footer() {
  return (
    <footer className="fk-footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-col">
            <h4>About</h4>
            <p>AJ Creations - Authentic Indian Handicrafts</p>
            <p>Supporting local artisans and traditional crafts</p>
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
  );
}

export default App;

