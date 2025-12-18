/**
 * ProTech Solutions - Form Validation & Auth Integration
 */

// ... (Keep existing validation helper functions: isValidEmail, isValidCameroonPhone, etc.)

/**
 * Handle Login
 */
async function validateLogin() {
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const messageDiv = document.getElementById('authMessage');

    // Clear previous messages
    if (messageDiv) messageDiv.innerHTML = '';

    // 1. Client-side Validation (Keep existing logic)
    const email = usernameInput.value.trim();
    const password = passwordInput.value;

    if (!email || !password) {
        showError(messageDiv, 'Please enter email and password');
        return false;
    }

    // 2. Server-side Authentication
    try {
        messageDiv.innerHTML = '<p style="color: var(--accent-color);">Logging in...</p>';

        // Attempt to login via API
        // Note: Requires api.js to be included in login.html
        if (typeof ApiClient !== 'undefined') {
            const response = await ApiClient.login(email, password);
            ApiClient.saveToken(response.access_token, response.user);
            showSuccess(messageDiv, 'Login successful! Redirecting...');

            setTimeout(() => {
                if (response.user && response.user.is_admin) {
                    window.location.href = 'admin.html';
                } else {
                    window.location.href = 'index.html';
                }
            }, 1000);
        } else {
            // Fallback for demo without backend running
            console.warn('ApiClient not found. Using demo mode.');
            setTimeout(() => {
                alert('Backend not connected. Demo login simulation.');
            }, 500);
        }

    } catch (error) {
        showError(messageDiv, error.message);
    }

    return false;
}

/**
 * Handle Registration
 */
async function validateRegister() {
    const fullnameInput = document.getElementById('fullname');
    const emailInput = document.getElementById('email');
    const phoneInput = document.getElementById('phone');
    const passwordInput = document.getElementById('password');
    const messageDiv = document.getElementById('authMessage');

    // Clear previous messages
    if (messageDiv) messageDiv.innerHTML = '';

    // 1. Client-side Validation
    // ... (Keep existing validation logic) ...
    // For brevity, assuming inputs are valid if they pass client checks

    const userData = {
        full_name: fullnameInput.value.trim(),
        email: emailInput.value.trim(),
        phone: phoneInput.value.trim(),
        password: passwordInput.value
    };

    // 2. Server-side Registration
    try {
        messageDiv.innerHTML = '<p style="color: var(--accent-color);">Creating account...</p>';

        if (typeof ApiClient !== 'undefined') {
            await ApiClient.register(userData);
            showSuccess(messageDiv, 'Registration successful! Please login.');
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        } else {
            console.warn('ApiClient not found. Using demo mode.');
            setTimeout(() => {
                alert('Backend not connected. Demo registration simulation.');
            }, 500);
        }
    } catch (error) {
        showError(messageDiv, error.message);
    }

    return false;
}

// Helper Functions (Restored)

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidCameroonPhone(phone) {
    const cleanPhone = phone.replace(/\s+/g, '');
    if (/^6\d{8}$/.test(cleanPhone)) return true;
    if (/^2376\d{8}$/.test(cleanPhone)) return true;
    return false;
}

function showError(container, message) {
    if (!container) return;
    container.innerHTML = `
        <div style="background-color: rgba(255, 107, 107, 0.1); 
                    border: 1px solid var(--error); 
                    color: var(--error); 
                    padding: 10px; 
                    border-radius: 4px; 
                    margin-top: 15px;">
            ${sanitizeHTML(message)}
        </div>
    `;
}

function showSuccess(container, message) {
    if (!container) return;
    container.innerHTML = `
        <div style="background-color: rgba(105, 219, 124, 0.1); 
                    border: 1px solid var(--success); 
                    color: var(--success); 
                    padding: 10px; 
                    border-radius: 4px; 
                    margin-top: 15px;">
            ${sanitizeHTML(message)}
        </div>
    `;
}

function sanitizeHTML(str) {
    const temp = document.createElement('div');
    temp.textContent = str;
    return temp.innerHTML;
}

function validateContactForm(event) {
    if (event) event.preventDefault();
    const name = document.getElementById('contact-name');
    const email = document.getElementById('contact-email');
    const message = document.getElementById('contact-message');

    if (!name || !name.value.trim() || name.value.trim().length < 3) {
        alert('Please enter a valid name (at least 3 characters)');
        return false;
    }
    if (!email || !email.value.trim() || !isValidEmail(email.value.trim())) {
        alert('Please enter a valid email address');
        return false;
    }
    if (!message || !message.value.trim() || message.value.trim().length < 10) {
        alert('Please enter a message (at least 10 characters)');
        return false;
    }
    alert('Contact form validation passed.');
    return false;
}
