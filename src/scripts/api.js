/**
 * ProTech Solutions - API Client
 * Handles communication with the Flask backend
 */

const API_BASE_URL = window.location.origin + '/api';

class ApiClient {
    /**
     * Get JWT token from local storage
     */
    static getToken() {
        return localStorage.getItem('access_token');
    }

    /**
     * Save JWT token details
     */
    static saveToken(token, user) {
        localStorage.setItem('access_token', token);
        if (user) {
            localStorage.setItem('user', JSON.stringify(user));
        }
    }

    /**
     * Clear token (Logout)
     */
    static logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        window.location.href = 'login.html';
    }

    /**
     * Generic fetch wrapper with enhanced error handling
     */
    static async request(endpoint, method = 'GET', data = null) {
        const headers = {
            'Content-Type': 'application/json'
        };

        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const config = {
            method,
            headers
        };

        if (data) {
            config.body = JSON.stringify(data);
        }

        const url = `${API_BASE_URL}${endpoint}`;
        console.log(`API Request: ${method} ${url}`);
        if (data) console.log('Request data:', data);

        try {
            const response = await fetch(url, config);
            console.log(`API Response status: ${response.status} ${response.statusText}`);

            // Try to parse JSON response
            let responseData;
            const contentType = response.headers.get('content-type');

            if (contentType && contentType.includes('application/json')) {
                responseData = await response.json();
                console.log('Response data:', responseData);
            } else {
                const text = await response.text();
                console.log('Response text:', text);
                responseData = { message: text };
            }

            if (!response.ok) {
                const errorMsg = responseData.message || responseData.msg || `HTTP ${response.status}: ${response.statusText}`;
                throw new Error(errorMsg);
            }

            return responseData;
        } catch (error) {
            console.error(`API Error (${method} ${endpoint}):`, error);

            // Enhance error message
            if (error.message.includes('Failed to fetch')) {
                throw new Error('Cannot connect to server. Please ensure the backend is running on http://127.0.0.1:5000');
            }

            throw error;
        }
    }

    // --- Specific API Calls ---

    static async login(email, password) {
        return this.request('/auth/login', 'POST', { email, password });
    }

    static async register(userData) {
        return this.request('/auth/register', 'POST', userData);
    }

    static async getProducts() {
        return this.request('/products/', 'GET');
    }

    static async getOrders() {
        return this.request('/orders/', 'GET');
    }

    static async createOrder(items) {
        return this.request('/orders/', 'POST', { items });
    }

    static async createProduct(productData) {
        return this.request('/products/', 'POST', productData);
    }

    static async updateProduct(productId, productData) {
        return this.request(`/products/${productId}`, 'PUT', productData);
    }

    static async deleteProduct(productId) {
        return this.request(`/products/${productId}`, 'DELETE');
    }

    static async updateStock(productId, stock) {
        return this.request(`/products/${productId}/stock`, 'PATCH', { stock });
    }

    static async updateOrderStatus(orderId, status) {
        return this.request(`/orders/${orderId}/status`, 'PATCH', { status });
    }

    static async getMyOrders() {
        return this.request('/orders/my-orders', 'GET');
    }

    static async getUsers() {
        return this.request('/users/', 'GET'); // Fixed endpoint
    }
}
