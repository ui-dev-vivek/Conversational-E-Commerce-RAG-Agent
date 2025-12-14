import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import apiService from '../api/apiService';
import './Cart.css';

function Cart() {
    const [cart, setCart] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        fetchCart();
    }, []);

    const fetchCart = async () => {
        try {
            setLoading(true);
            const data = await apiService.getCart();
            setCart(data);
        } catch (err) {
            console.error('Failed to load cart:', err);
            if (err.message.includes('Invalid')) {
                navigate('/login');
            }
        } finally {
            setLoading(false);
        }
    };

    const handleUpdateQuantity = async (cartItemId, newQuantity) => {
        try {
            await apiService.updateCartItem(cartItemId, newQuantity);
            fetchCart();
        } catch (err) {
            alert('Failed to update quantity: ' + err.message);
        }
    };

    const handleRemoveItem = async (cartItemId) => {
        try {
            await apiService.removeFromCart(cartItemId);
            fetchCart();
        } catch (err) {
            alert('Failed to remove item: ' + err.message);
        }
    };

    const handleCheckout = () => {
        if (cart && cart.items.length > 0) {
            navigate('/checkout');
        }
    };

    if (loading) {
        return <div className="loading">Loading cart...</div>;
    }

    if (!cart || cart.items.length === 0) {
        return (
            <div className="empty-cart">
                <h2>Your cart is empty</h2>
                <p>Add some products to get started!</p>
                <button onClick={() => navigate('/products')}>
                    Browse Products
                </button>
            </div>
        );
    }

    return (
        <div className="cart-page">
            <h1>Shopping Cart ({cart.item_count} items)</h1>

            <div className="cart-container">
                <div className="cart-items">
                    {cart.items.map(item => (
                        <div key={item.id} className="cart-item">
                            <img src={item.product_image} alt={item.product_name} />
                            <div className="item-details">
                                <h3>{item.product_name}</h3>
                                <p className="item-price">
                                    {item.currency} {item.price.toFixed(2)}
                                </p>
                                <p className="stock-info">
                                    {item.stock > 0 ? `${item.stock} available` : 'Out of stock'}
                                </p>
                            </div>
                            <div className="item-actions">
                                <div className="quantity-controls">
                                    <button
                                        onClick={() => handleUpdateQuantity(item.id, item.quantity - 1)}
                                        disabled={item.quantity <= 1}
                                    >
                                        -
                                    </button>
                                    <span>{item.quantity}</span>
                                    <button
                                        onClick={() => handleUpdateQuantity(item.id, item.quantity + 1)}
                                        disabled={item.quantity >= item.stock}
                                    >
                                        +
                                    </button>
                                </div>
                                <p className="item-total">
                                    Total: {item.currency} {item.item_total.toFixed(2)}
                                </p>
                                <button
                                    className="remove-btn"
                                    onClick={() => handleRemoveItem(item.id)}
                                >
                                    Remove
                                </button>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="cart-summary">
                    <h2>Order Summary</h2>
                    <div className="summary-row">
                        <span>Subtotal ({cart.item_count} items):</span>
                        <span>{cart.currency} {cart.total.toFixed(2)}</span>
                    </div>
                    <div className="summary-row">
                        <span>Shipping:</span>
                        <span className="free">FREE</span>
                    </div>
                    <div className="summary-row total">
                        <span>Total:</span>
                        <span>{cart.currency} {cart.total.toFixed(2)}</span>
                    </div>
                    <button className="checkout-btn" onClick={handleCheckout}>
                        Proceed to Checkout
                    </button>
                    <button
                        className="continue-shopping"
                        onClick={() => navigate('/products')}
                    >
                        Continue Shopping
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Cart;
