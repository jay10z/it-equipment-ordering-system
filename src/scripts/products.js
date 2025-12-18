/**
 * ProTech Solutions - Products Module
 * Contains product data and rendering functions
 */

// Global products array
let allProducts = [];

/**
 * Initialize products
 */
async function initProducts() {
    try {
        if (typeof ApiClient !== 'undefined') {
            console.log('Fetching products from API...');
            const products = await ApiClient.getProducts();
            if (products && products.length > 0) {
                allProducts = products;
                console.log('Products loaded from API:', allProducts.length);
            } else {
                throw new Error('No products returned from API');
            }
        } else {
            throw new Error('ApiClient not defined');
        }
    } catch (error) {
        console.warn('API unavailable, using fallback data:', error.message);
        // Fallback products
        allProducts = [
            { id: 1, name: 'Dell Latitude 5420', category: 'Computers', price: 450000, availability: 'In Stock', warranty: '12 months', specs: '14" FHD, Intel i5-1135G7, 8GB RAM, 256GB SSD', image: null },
            { id: 2, name: 'HP ProBook 450 G8', category: 'Computers', price: 520000, availability: 'In Stock', warranty: '12 months', specs: '15.6" FHD, Intel i7-1165G7, 16GB RAM, 512GB SSD', image: null },
            { id: 3, name: 'Lenovo ThinkPad T14', category: 'Computers', price: 480000, availability: 'Limited Stock', warranty: '12 months', specs: '14" FHD, AMD Ryzen 5, 8GB RAM, 256GB SSD', image: null },
            { id: 4, name: 'Cisco Small Business Router', category: 'Networking', price: 95000, availability: 'In Stock', warranty: '24 months', specs: 'Dual-band, 5 Gigabit ports, VPN support', image: null },
            { id: 5, name: 'TP-Link 24-Port Switch', category: 'Networking', price: 120000, availability: 'In Stock', warranty: '36 months', specs: '10/100/1000 Mbps, Rackmount, Unmanaged', image: null },
            { id: 6, name: 'Ubiquiti UniFi AP AC Pro', category: 'Networking', price: 85000, availability: 'In Stock', warranty: '12 months', specs: 'Dual-band WiFi, PoE, up to 450 Mbps', image: null },
            { id: 7, name: 'Logitech MX Master 3', category: 'Accessories', price: 35000, availability: 'In Stock', warranty: '12 months', specs: 'Wireless Mouse, 7 buttons, 4000 DPI', image: null },
            { id: 8, name: 'Logitech MX Keys', category: 'Accessories', price: 45000, availability: 'In Stock', warranty: '12 months', specs: 'Wireless Keyboard, Backlit, USB-C charging', image: null },
            { id: 9, name: 'HDMI Cable 2m', category: 'Accessories', price: 3500, availability: 'In Stock', warranty: '6 months', specs: '4K support, High speed, Gold plated', image: null },
            { id: 10, name: 'Seagate Backup Plus 2TB', category: 'Storage', price: 45000, availability: 'In Stock', warranty: '24 months', specs: 'External HDD, USB 3.0, Portable', image: null },
            { id: 11, name: 'Samsung T7 SSD 1TB', category: 'Storage', price: 95000, availability: 'In Stock', warranty: '36 months', specs: 'External SSD, USB 3.2, 1050 MB/s read', image: null },
            { id: 12, name: 'SanDisk Ultra 128GB USB', category: 'Storage', price: 7500, availability: 'In Stock', warranty: '12 months', specs: 'USB 3.0, 130 MB/s read speed', image: null }
        ];
    }

    // Trigger render if on a page that needs it
    const productsGrid = document.getElementById('products-grid');
    const featuredProducts = document.getElementById('featured-products');

    if (productsGrid) {
        renderProducts(allProducts, 'products-grid');
    }

    if (featuredProducts) {
        renderProducts(allProducts.slice(0, 6), 'featured-products');
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', initProducts);

/**
 * Render products to a container
 */
function renderProducts(products, containerId) {
    const container = document.getElementById(containerId);

    if (!container) {
        console.error('Container not found:', containerId);
        return;
    }

    container.innerHTML = '';

    if (products.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No products found in this category.</p>';
        return;
    }

    products.forEach(product => {
        const productCard = createProductCard(product);
        container.appendChild(productCard);
    });
}

/**
 * Create a product card element
 */
function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card';

    card.innerHTML = `
        <div class="product-image">
            ${product.image ? `<img src="${product.image}" alt="${product.name}">` : '<i class="fa fa-laptop" style="font-size: 4rem;"></i>'}
        </div>
        <div class="product-info">
            <span class="product-category">${product.category}</span>
            <h3 class="product-title">${sanitizeHTML(product.name)}</h3>
            <span class="product-price">${formatPrice(product.price)} FCFA</span>
            <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 10px;">${sanitizeHTML(product.specs)}</p>
            <p style="font-size: 0.8rem; color: var(--success);">${sanitizeHTML(product.availability)}</p>
            <button class="btn-add-cart" data-product-id="${product.id}">
                <i class="fa fa-shopping-cart"></i> Add to Cart
            </button>
        </div>
    `;

    // Add event listener to the button
    const btn = card.querySelector('.btn-add-cart');
    btn.addEventListener('click', function () {
        const productId = this.getAttribute('data-product-id');
        addToCart(productId);
    });

    return card;
}

/**
 * Format price with thousand separators
 */
function formatPrice(price) {
    return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}

/**
 * Basic HTML sanitization to prevent XSS
 */
function sanitizeHTML(str) {
    const temp = document.createElement('div');
    temp.textContent = str;
    return temp.innerHTML;
}

/**
 * Add product to cart (uses localStorage)
 */
function addToCart(productId) {
    console.log('addToCart called with ID:', productId, 'Type:', typeof productId);

    // Validate productId
    if (!productId) {
        alert('Invalid product ID');
        return;
    }

    // Ensure allProducts is populated
    if (!allProducts || allProducts.length === 0) {
        console.error('Product database not loaded yet.');
        alert('Please wait, loading products...');
        return;
    }

    // Find the product (convert both to numbers for comparison)
    const product = allProducts.find(p => Number(p.id) === Number(productId));

    if (!product) {
        console.error('Product not found in local list. ID:', productId);
        console.log('Available products:', allProducts.map(p => p.id));
        alert('Product not found in catalog.');
        return;
    }

    console.log('Found product:', product.name);

    // Get existing cart from localStorage
    let cart = [];
    try {
        const cartData = localStorage.getItem('cart');
        if (cartData) {
            cart = JSON.parse(cartData);
        }
    } catch (error) {
        console.error('Error reading cart:', error);
        cart = [];
    }

    // Check if product already in cart
    const existingItem = cart.find(item => Number(item.id) === Number(productId));

    if (existingItem) {
        existingItem.quantity += 1;
        console.log('Incremented quantity for:', product.name);
    } else {
        cart.push({
            id: Number(product.id),
            name: product.name,
            price: product.price,
            quantity: 1
        });
        console.log('Added new item:', product.name);
    }

    // Save to localStorage
    try {
        localStorage.setItem('cart', JSON.stringify(cart));
        alert(`✓ ${product.name} added to cart!`);
        console.log('Cart saved successfully. Total items:', cart.length);
    } catch (error) {
        alert('Error adding to cart. Please try again.');
        console.error('Error saving cart:', error);
    }
}

// Make addToCart globally accessible
window.addToCart = addToCart;
