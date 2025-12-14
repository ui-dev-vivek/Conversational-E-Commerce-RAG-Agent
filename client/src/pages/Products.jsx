import { useState, useEffect } from 'react';
import apiService from '../api/apiService';
import './Products.css';

function Products({ onAddToCart }) {
    const [productsByCategory, setProductsByCategory] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedCategory, setSelectedCategory] = useState('All');

    useEffect(() => {
        fetchProducts();
    }, []);

    const fetchProducts = async () => {
        try {
            setLoading(true);
            const data = await apiService.getProductsByCategory();
            setProductsByCategory(data);
            setError(null);
        } catch (err) {
            setError('Failed to load products');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleAddToCart = async (productId, productName) => {
        const token = localStorage.getItem('token');

        if (!token) {
            alert('Please login to add items to cart');
            window.location.href = '/login';
            return;
        }

        try {
            await apiService.addToCart(productId, 1);
            alert(`${productName} added to cart!`);
            if (onAddToCart) onAddToCart();
        } catch (err) {
            alert('Failed to add to cart: ' + err.message);
        }
    };

    const categories = Object.keys(productsByCategory);
    const filteredCategories = selectedCategory === 'All'
        ? categories
        : categories.filter(cat => cat === selectedCategory);

    if (loading) {
        return <div className="loading">Loading products...</div>;
    }

    if (error) {
        return <div className="error">{error}</div>;
    }

    return (
        <div className="products-page">
            {/* Header */}
            <div className="products-header">
                <h1>🛍️ Our Products</h1>
                <p>Browse our amazing collection</p>
            </div>

            {/* Category Filter */}
            <div className="category-filter">
                <button
                    className={`filter-btn ${selectedCategory === 'All' ? 'active' : ''}`}
                    onClick={() => setSelectedCategory('All')}
                >
                    ✨ All Products
                </button>
                {categories.map(category => (
                    <button
                        key={category}
                        className={`filter-btn ${selectedCategory === category ? 'active' : ''}`}
                        onClick={() => setSelectedCategory(category)}
                    >
                        {category.replace(/_/g, ' ').replace(/\w\S*/g, function (txt) {
                            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
                        })}
                    </button>
                ))}
            </div>

            {/* Products by Category */}
            {filteredCategories.length > 0 ? (
                filteredCategories.map(category => (
                    <div key={category} className="category-section">
                        <div className="category-header">
                            <h2 className="category-title">{category.replace(/_/g, ' ').replace(/\w\S*/g, function (txt) {
                                return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
                            })}</h2>
                            <p className="category-description">
                                {productsByCategory[category]?.category_description || ''}
                            </p>
                        </div>

                        <div className="product-grid">
                            {productsByCategory[category]?.products?.map(product => (
                                <div key={product.id} className="product-card">
                                    {/* Image Container */}
                                    <div className="product-image-container">
                                        <img
                                            src={`https://placehold.co/300x300?text=${product.name.replace(/ /g, '+')}`}
                                            alt={product.name}
                                            className="product-image"
                                        />
                                        {product.stock === 0 && (
                                            <div className="stock-badge">Out of Stock</div>
                                        )}
                                    </div>

                                    {/* Product Info */}
                                    <div className="product-info">
                                        <h3 className="product-name">{product.name}</h3>
                                        <p className="product-description">{product.description}</p>

                                        {product.material && (
                                            <p className="product-material">
                                                📦 Material: {product.material}
                                            </p>
                                        )}

                                        {product.rating && (
                                            <div className="product-rating">
                                                ⭐ {product.rating}/5
                                            </div>
                                        )}

                                        {/* Stock Info */}
                                        <p className={`stock-info ${product.stock > 0 ? 'in-stock' : 'out-of-stock'}`}>
                                            {product.stock > 0 ? `✓ ${product.stock} in stock` : '✗ Out of stock'}
                                        </p>

                                        {/* Footer */}
                                        <div className="product-footer">
                                            <span className="price">
                                                {product.currency} {product.price.toFixed(2)}
                                            </span>
                                            <button
                                                className="add-to-cart-btn"
                                                onClick={() => handleAddToCart(product.id, product.name)}
                                                disabled={product.stock === 0}
                                            >
                                                {product.stock > 0 ? '🛒 Add to Cart' : 'Out of Stock'}
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                ))
            ) : (
                <div className="no-products">No products found</div>
            )}
        </div>
    );
}

export default Products;
