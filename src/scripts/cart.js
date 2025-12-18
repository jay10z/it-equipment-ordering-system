/**
 * ProTech Solutions - Shopping Cart Module
 * Handles cart display and management
 */

// ------------------
// Global Helpers
// ------------------

// Helper to save cart
function saveCart(cart) {
    try {
        localStorage.setItem('cart', JSON.stringify(cart));
    } catch (e) {
        console.error("Error saving cart", e);
    }
}

// Helper to get cart
function getCart() {
    try {
        const c = localStorage.getItem('cart');
        return c ? JSON.parse(c) : [];
    } catch {
        return [];
    }
}

// Helper to format price
function formatPrice(price) {
    return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}

// Helper to sanitize HTML
function sanitizeHTML(str) {
    const temp = document.createElement('div');
    temp.textContent = str;
    return temp.innerHTML;
}

/**
 * Load and display cart items (renamed to renderCart to match usage)
 */
window.renderCart = function () {
    const cartItemsContainer = document.getElementById('cart-items');
    const cartTotalElement = document.getElementById('cart-total');
    const cartSubtotalElement = document.getElementById('cart-subtotal');

    if (!cartItemsContainer || !cartTotalElement) {
        // This might run on pages without a cart, which is fine
        return;
    }

    const cart = getCart();

    // Clear container
    cartItemsContainer.innerHTML = '';

    // Check if cart is empty
    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">Your cart is currently empty.</p>';
        cartTotalElement.textContent = '0 FCFA';
        if (cartSubtotalElement) cartSubtotalElement.textContent = '0 FCFA';
        return;
    }

    // Calculate total
    let total = 0;

    // Render cart items
    cart.forEach((item, index) => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;

        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item';
        cartItem.innerHTML = `
            <div class="cart-item-info">
                <h3>${sanitizeHTML(item.name)}</h3>
                <p>Price: ${formatPrice(item.price)} FCFA</p>
            </div>
            <div class="cart-item-controls">
                <button onclick="updateQuantity(${index}, -1)">-</button>
                <span>${item.quantity}</span>
                <button onclick="updateQuantity(${index}, 1)">+</button>
            </div>
            <div class="cart-item-total">
                <p>${formatPrice(itemTotal)} FCFA</p>
                <button class="remove-btn" onclick="removeItem(${index})">
                    <i class="fa fa-trash"></i>
                </button>
            </div>
        `;

        cartItemsContainer.appendChild(cartItem);
    });

    // Update total and subtotal
    const formattedTotal = formatPrice(total) + ' FCFA';
    cartTotalElement.textContent = formattedTotal;
    if (cartSubtotalElement) cartSubtotalElement.textContent = formattedTotal;
};

/**
 * Update item quantity in cart
 */
window.updateQuantity = function (index, change) {
    if (isNaN(index) || isNaN(change)) return;

    const cart = getCart();
    if (index < 0 || index >= cart.length) return;

    cart[index].quantity += change;
    if (cart[index].quantity <= 0) {
        cart.splice(index, 1);
    }

    saveCart(cart);
    renderCart();
};

/**
 * Remove item from cart
 */
window.removeItem = function (index) {
    if (isNaN(index)) return;

    const cart = getCart();
    if (index < 0 || index >= cart.length) return;

    if (confirm('Remove this item from cart?')) {
        cart.splice(index, 1);
        saveCart(cart);
        renderCart();
    }
};

/**
 * Checkout Handler - WITH DETAILED ERROR LOGGING
 */
window.handleCheckout = async function () {
    console.log("=== CHECKOUT PROCESS STARTED ===");
    console.log("Time:", new Date().toISOString());

    // Step 1: Check ApiClient
    if (typeof ApiClient === 'undefined') {
        console.error("❌ ApiClient is not defined!");
        alert("System Error: API Client missing. Please refresh the page.");
        return;
    }
    console.log("✓ ApiClient is available");

    // Step 2: Check authentication
    const token = ApiClient.getToken();
    console.log("Token exists:", !!token);
    console.log("Token value:", token ? token.substring(0, 20) + "..." : "null");

    if (!token) {
        console.error("❌ No authentication token found");
        alert("Please log in to complete your purchase.");
        window.location.href = 'login.html';
        return;
    }
    console.log("✓ User is authenticated");

    // Step 3: Get cart data
    const cart = getCart();
    console.log("Cart items count:", cart.length);
    console.log("Cart contents:", cart);

    if (cart.length === 0) {
        console.error("❌ Cart is empty");
        alert("Your cart is empty!");
        return;
    }
    console.log("✓ Cart has items");

    // Step 4: Prepare order data
    const orderItems = cart.map(item => ({
        id: Number(item.id),
        quantity: Number(item.quantity)
    }));
    console.log("Order items prepared:", orderItems);

    // Step 5: Update UI
    const checkoutBtn = document.querySelector('.checkout-btn');
    const originalText = checkoutBtn ? checkoutBtn.textContent : '';

    if (checkoutBtn) {
        checkoutBtn.textContent = 'Processing...';
        checkoutBtn.disabled = true;
    }

    try {
        console.log("=== SENDING REQUEST TO BACKEND ===");
        console.log("API URL:", 'http://127.0.0.1:5000/api/orders/');
        console.log("Request data:", { items: orderItems });

        // Step 6: Send to backend
        const result = await ApiClient.createOrder(orderItems);

        console.log("=== BACKEND RESPONSE RECEIVED ===");
        console.log("Response:", result);

        // Step 7: Success handling
        if (result && result.order_id) {
            console.log("✅ Order created successfully!");
            console.log("Order ID:", result.order_id);
            console.log("Total:", result.total);

            alert(`✅ Order Placed Successfully!\n\nOrder ID: #${result.order_id}\nTotal: ${result.total.toLocaleString()} FCFA\n\nThank you for your purchase!`);

            // Clear cart
            saveCart([]);
            renderCart();

            if (checkoutBtn) {
                checkoutBtn.textContent = 'Order Placed ✓';
                setTimeout(() => {
                    checkoutBtn.textContent = originalText;
                    checkoutBtn.disabled = false;
                }, 3000);
            }
        } else {
            throw new Error("Invalid response from server");
        }

    } catch (error) {
        console.error("=== CHECKOUT ERROR ===");
        console.error("Error type:", error.constructor.name);
        console.error("Error message:", error.message);
        console.error("Full error:", error);

        // Check for specific error types
        let errorMessage = "Checkout Failed: ";

        if (error.message.includes("Failed to fetch") || error.message.includes("NetworkError")) {
            errorMessage += "Cannot connect to server. Please ensure the backend is running.";
            console.error("❌ Network error - backend may not be running");
        } else if (error.message.includes("401") || error.message.includes("Unauthorized")) {
            errorMessage += "Authentication failed. Please log in again.";
            console.error("❌ Authentication error");
        } else if (error.message.includes("400")) {
            errorMessage += "Invalid request. Please check your cart items.";
            console.error("❌ Bad request error");
        } else {
            errorMessage += error.message;
        }

        alert(errorMessage);

        if (checkoutBtn) {
            checkoutBtn.textContent = originalText;
            checkoutBtn.disabled = false;
        }
    }

    console.log("=== CHECKOUT PROCESS ENDED ===");
};

// Bind to button
document.addEventListener('DOMContentLoaded', () => {
    // Alias loadCart to renderCart for compatibility
    window.loadCart = window.renderCart;
    renderCart();

    // Attach event listener to checkout button
    const btn = document.querySelector('.checkout-btn');
    if (btn) {
        btn.addEventListener('click', handleCheckout);
    }

    console.log("Cart module loaded. Cart items:", getCart().length);
});
