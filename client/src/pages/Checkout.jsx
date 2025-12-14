import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import apiService from '../api/apiService';
import './Checkout.css';

function Checkout() {
    const [cart, setCart] = useState(null);
    const [order, setOrder] = useState(null);
    const [step, setStep] = useState('review'); // review, payment, result
    const [paymentData, setPaymentData] = useState({
        card_number: '',
        card_holder: '',
        expiry_date: '',
        cvv: '',
        billing_address: ''
    });
    const [paymentResult, setPaymentResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        fetchCart();
    }, []);

    const fetchCart = async () => {
        try {
            const data = await apiService.getCart();
            setCart(data);

            if (data.items.length === 0) {
                navigate('/cart');
            }
        } catch (err) {
            console.error('Failed to load cart:', err);
            navigate('/login');
        }
    };

    const handleCreateOrder = async () => {
        try {
            setLoading(true);
            const orderData = await apiService.createOrder();
            setOrder(orderData);
            setStep('payment');
        } catch (err) {
            alert('Failed to create order: ' + err.message);
        } finally {
            setLoading(false);
        }
    };

    const handlePaymentChange = (e) => {
        setPaymentData({
            ...paymentData,
            [e.target.name]: e.target.value
        });
    };

    const handlePayment = async (e) => {
        e.preventDefault();

        if (!order) return;

        try {
            setLoading(true);
            const result = await apiService.processPayment(order.order_id, paymentData);
            setPaymentResult(result);
            setStep('result');
        } catch (err) {
            alert('Payment processing failed: ' + err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleRetryPayment = async () => {
        try {
            setLoading(true);
            const result = await apiService.retryPayment(order.order_id, paymentData);
            setPaymentResult(result);
        } catch (err) {
            alert('Payment retry failed: ' + err.message);
        } finally {
            setLoading(false);
        }
    };

    if (!cart) {
        return <div className="loading">Loading...</div>;
    }

    return (
        <div className="checkout-page">
            <div className="checkout-container">
                {/* Progress Steps */}
                <div className="checkout-steps">
                    <div className={`step ${step === 'review' ? 'active' : 'completed'}`}>
                        <span className="step-number">1</span>
                        <span className="step-label">Review Order</span>
                    </div>
                    <div className={`step ${step === 'payment' ? 'active' : step === 'result' ? 'completed' : ''}`}>
                        <span className="step-number">2</span>
                        <span className="step-label">Payment</span>
                    </div>
                    <div className={`step ${step === 'result' ? 'active' : ''}`}>
                        <span className="step-number">3</span>
                        <span className="step-label">Confirmation</span>
                    </div>
                </div>

                {/* Review Step */}
                {step === 'review' && (
                    <div className="review-section">
                        <h2>Review Your Order</h2>
                        <div className="order-items">
                            {cart.items.map(item => (
                                <div key={item.id} className="order-item">
                                    <img src={item.product_image} alt={item.product_name} />
                                    <div className="item-info">
                                        <h3>{item.product_name}</h3>
                                        <p>Quantity: {item.quantity}</p>
                                        <p className="price">{item.currency} {item.item_total.toFixed(2)}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                        <div className="order-total">
                            <h3>Total Amount: {cart.currency} {cart.total.toFixed(2)}</h3>
                        </div>
                        <button
                            className="proceed-btn"
                            onClick={handleCreateOrder}
                            disabled={loading}
                        >
                            {loading ? 'Creating Order...' : 'Proceed to Payment'}
                        </button>
                    </div>
                )}

                {/* Payment Step */}
                {step === 'payment' && order && (
                    <div className="payment-section">
                        <h2>Payment Details</h2>
                        <div className="order-info">
                            <p><strong>Order Number:</strong> {order.order_number}</p>
                            <p><strong>Amount:</strong> INR {order.total_amount.toFixed(2)}</p>
                        </div>

                        <div className="payment-tip">
                            <p>💡 <strong>Testing Tip:</strong> Use card number ending with <strong>even digit</strong> for success, <strong>odd digit</strong> for failure</p>
                            <p>Example: 4242424242424242 (success) or 4242424242424241 (failure)</p>
                        </div>

                        <form onSubmit={handlePayment} className="payment-form">
                            <div className="form-group">
                                <label>Card Number</label>
                                <input
                                    type="text"
                                    name="card_number"
                                    value={paymentData.card_number}
                                    onChange={handlePaymentChange}
                                    placeholder="1234 5678 9012 3456"
                                    required
                                    maxLength="16"
                                />
                            </div>

                            <div className="form-group">
                                <label>Card Holder Name</label>
                                <input
                                    type="text"
                                    name="card_holder"
                                    value={paymentData.card_holder}
                                    onChange={handlePaymentChange}
                                    placeholder="John Doe"
                                    required
                                />
                            </div>

                            <div className="form-row">
                                <div className="form-group">
                                    <label>Expiry Date</label>
                                    <input
                                        type="text"
                                        name="expiry_date"
                                        value={paymentData.expiry_date}
                                        onChange={handlePaymentChange}
                                        placeholder="MM/YY"
                                        required
                                    />
                                </div>

                                <div className="form-group">
                                    <label>CVV</label>
                                    <input
                                        type="text"
                                        name="cvv"
                                        value={paymentData.cvv}
                                        onChange={handlePaymentChange}
                                        placeholder="123"
                                        required
                                        maxLength="3"
                                    />
                                </div>
                            </div>

                            <div className="form-group">
                                <label>Billing Address</label>
                                <textarea
                                    name="billing_address"
                                    value={paymentData.billing_address}
                                    onChange={handlePaymentChange}
                                    placeholder="Enter your billing address"
                                    required
                                    rows="3"
                                />
                            </div>

                            <button type="submit" className="pay-btn" disabled={loading}>
                                {loading ? 'Processing...' : `Pay INR ${order.total_amount.toFixed(2)}`}
                            </button>
                        </form>
                    </div>
                )}

                {/* Result Step */}
                {step === 'result' && paymentResult && (
                    <div className="result-section">
                        {paymentResult.success ? (
                            <div className="success-result">
                                <div className="success-icon">✓</div>
                                <h2>Payment Successful!</h2>
                                <p>{paymentResult.message}</p>
                                <div className="order-details">
                                    <p><strong>Order Number:</strong> {paymentResult.order_number}</p>
                                    <p><strong>Tracking ID:</strong> {paymentResult.tracking_id}</p>
                                    <p><strong>Estimated Delivery:</strong> {paymentResult.estimated_delivery}</p>
                                    <p><strong>Status:</strong> <span className="status-confirmed">{paymentResult.status}</span></p>
                                </div>
                                <button onClick={() => navigate('/products')} className="continue-btn">
                                    Continue Shopping
                                </button>
                            </div>
                        ) : (
                            <div className="failure-result">
                                <div className="failure-icon">✗</div>
                                <h2>Payment Failed</h2>
                                <p>{paymentResult.message}</p>
                                <div className="order-details">
                                    <p><strong>Order Number:</strong> {paymentResult.order_number}</p>
                                    <p><strong>Status:</strong> <span className="status-failed">{paymentResult.status}</span></p>
                                </div>
                                <div className="failure-actions">
                                    <button onClick={handleRetryPayment} className="retry-btn" disabled={loading}>
                                        {loading ? 'Processing...' : 'Retry Payment'}
                                    </button>
                                    <button onClick={() => navigate('/cart')} className="back-btn">
                                        Back to Cart
                                    </button>
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

export default Checkout;
