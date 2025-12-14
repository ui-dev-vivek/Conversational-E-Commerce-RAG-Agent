// API service for all backend calls
const API_BASE_URL = 'http://localhost:8000/api';

class ApiService {
    constructor() {
        this.token = localStorage.getItem('token');
    }

    setToken(token) {
        this.token = token;
        localStorage.setItem('token', token);
    }

    clearToken() {
        this.token = null;
        localStorage.removeItem('token');
    }

    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };

        const config = {
            ...options,
            headers,
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Auth APIs
    async register(userData) {
        const data = await this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData),
        });
        this.setToken(data.access_token);
        return data;
    }

    async login(credentials) {
        const data = await this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify(credentials),
        });
        this.setToken(data.access_token);
        return data;
    }

    async getCurrentUser() {
        return this.request(`/auth/me?token=${this.token}`);
    }

    // Product APIs
    async getProducts(category = null, search = null) {
        let endpoint = '/products/';
        const params = new URLSearchParams();
        if (category) params.append('category', category);
        if (search) params.append('search', search);
        if (params.toString()) endpoint += `?${params.toString()}`;

        return this.request(endpoint);
    }

    async getProductsByCategory() {
        return this.request('/products/by-category');
    }

    async getProduct(productId) {
        return this.request(`/products/${productId}`);
    }

    // Cart APIs
    async getCart() {
        return this.request(`/cart/?token=${this.token}`);
    }

    async addToCart(productId, quantity = 1) {
        return this.request(`/cart/add?token=${this.token}`, {
            method: 'POST',
            body: JSON.stringify({ product_id: productId, quantity }),
        });
    }

    async updateCartItem(cartItemId, quantity) {
        return this.request(`/cart/${cartItemId}?token=${this.token}`, {
            method: 'PUT',
            body: JSON.stringify({ quantity }),
        });
    }

    async removeFromCart(cartItemId) {
        return this.request(`/cart/${cartItemId}?token=${this.token}`, {
            method: 'DELETE',
        });
    }

    async clearCart() {
        return this.request(`/cart/clear?token=${this.token}`, {
            method: 'DELETE',
        });
    }

    // Order APIs
    async createOrder() {
        return this.request(`/orders/create?token=${this.token}`, {
            method: 'POST',
        });
    }

    async getOrders() {
        return this.request(`/orders/?token=${this.token}`);
    }

    async getOrder(orderId) {
        return this.request(`/orders/${orderId}?token=${this.token}`);
    }

    async processPayment(orderId, paymentData) {
        return this.request(`/orders/${orderId}/payment?token=${this.token}`, {
            method: 'POST',
            body: JSON.stringify(paymentData),
        });
    }

    async retryPayment(orderId, paymentData) {
        return this.request(`/orders/${orderId}/retry-payment?token=${this.token}`, {
            method: 'POST',
            body: JSON.stringify(paymentData),
        });
    }
}

export default new ApiService();
