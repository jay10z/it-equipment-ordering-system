# 🔧 CHECKOUT ERROR DEBUGGING GUIDE

## Problem: "Checkout Failed: API request failed"

This guide will help you identify and fix the checkout error.

---

## 🔍 Step-by-Step Debugging Process

### **Step 1: Open Browser Developer Console**

1. Open your browser (Chrome, Firefox, Edge, Safari)
2. Press **F12** (or Right-click → Inspect)
3. Click on the **"Console"** tab
4. Keep it open while testing

### **Step 2: Refresh the Page**

1. Press **Ctrl+Shift+R** (Windows/Linux) or **Cmd+Shift+R** (Mac)
2. This clears the cache and loads the latest JavaScript

### **Step 3: Check Initial Logs**

When the page loads, you should see in the console:
```
Cart module loaded. Cart items: X
```

If you don't see this, the cart.js file isn't loading properly.

### **Step 4: Add Items to Cart**

1. Go to Products page
2. Click "Add to Cart" on a product
3. **Check Console** - you should see:
```
addToCart called with ID: 1
Found product: Dell Latitude 5420
Cart saved successfully. Total items: 1
```

### **Step 5: Go to Cart Page**

Navigate to `cart.html`. The cart should display your items.

### **Step 6: Attempt Checkout**

Click "Proceed to Checkout" and **watch the console carefully**. You should see detailed logs like:

#### **✅ SUCCESSFUL CHECKOUT LOGS:**
```
=== CHECKOUT PROCESS STARTED ===
Time: 2025-12-18T00:09:07.123Z
✓ ApiClient is available
Token exists: true
Token value: eyJhbGciOiJIUzI1NiIs...
✓ User is authenticated
Cart items count: 2
Cart contents: [{id: 1, name: "Dell...", quantity: 2}, ...]
✓ Cart has items
Order items prepared: [{id: 1, quantity: 2}, ...]
=== SENDING REQUEST TO BACKEND ===
API URL: http://127.0.0.1:5000/api/orders/
Request data: {items: [{id: 1, quantity: 2}, ...]}
API Request: POST http://127.0.0.1:5000/api/orders/
API Response status: 201 Created
Response data: {message: "Order placed successfully", order_id: 1, total: 900000}
=== BACKEND RESPONSE RECEIVED ===
Response: {message: "Order placed successfully", order_id: 1, total: 900000}
✅ Order created successfully!
Order ID: 1
Total: 900000
=== CHECKOUT PROCESS ENDED ===
```

#### **❌ ERROR SCENARIOS:**

##### **Error 1: ApiClient Not Defined**
```
❌ ApiClient is not defined!
```
**Fix**: Ensure `<script src="scripts/api.js"></script>` is in cart.html BEFORE cart.js

##### **Error 2: No Authentication Token**
```
Token exists: false
❌ No authentication token found
```
**Fix**: You're not logged in. Go to login.html and log in first.

##### **Error 3: Cannot Connect to Server**
```
API Request: POST http://127.0.0.1:5000/api/orders/
❌ Network error - backend may not be running
Error: Cannot connect to server
```
**Fix**: Backend is not running. Start it:
```bash
cd backend
source venv/bin/activate
python app.py
```

##### **Error 4: CORS Error**
```
Access to fetch at 'http://127.0.0.1:5000/api/orders/' from origin 'file://' 
has been blocked by CORS policy
```
**Fix**: Backend CORS is not configured. Check `backend/app/__init__.py` has:
```python
cors.init_app(app)
```

##### **Error 5: 401 Unauthorized**
```
API Response status: 401 Unauthorized
❌ Authentication error
```
**Fix**: Token is invalid or expired. Log out and log in again.

##### **Error 6: 400 Bad Request**
```
API Response status: 400 Bad Request
Response data: {message: "No items provided"}
```
**Fix**: Cart data format is wrong. Check cart items structure.

---

## 🛠️ Common Fixes

### **Fix 1: Restart Backend Server**

The most common issue is the backend not running or crashed.

```bash
# Kill any existing processes on port 5000
lsof -ti:5000 | xargs kill -9

# Navigate to backend
cd backend

# Activate virtual environment
source venv/bin/activate

# Start server
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### **Fix 2: Clear Browser Cache**

Old JavaScript files might be cached.

1. Press **Ctrl+Shift+Delete** (or **Cmd+Shift+Delete** on Mac)
2. Select "Cached images and files"
3. Click "Clear data"
4. Or just press **Ctrl+Shift+R** to hard refresh

### **Fix 3: Verify Login Status**

1. Open Console
2. Type: `localStorage.getItem('access_token')`
3. If it returns `null`, you're not logged in
4. If it returns a long string, you're logged in

### **Fix 4: Check Cart Data**

1. Open Console
2. Type: `localStorage.getItem('cart')`
3. You should see: `[{"id":1,"name":"Dell...","price":450000,"quantity":1}]`
4. If it's `null` or `[]`, your cart is empty

### **Fix 5: Manually Test API**

Open a new terminal and test the API directly:

```bash
# Test if backend is responding
curl http://127.0.0.1:5000/api/products

# You should get JSON response with products
```

---

## 📋 Checklist Before Checkout

- [ ] Backend server is running (`python app.py`)
- [ ] You see "Running on http://127.0.0.1:5000" in terminal
- [ ] You are logged in (navbar shows "Logout" not "Login")
- [ ] Cart has items (cart page shows products)
- [ ] Browser console is open (F12)
- [ ] No red errors in console before clicking checkout

---

## 🧪 Test Sequence

Follow this exact sequence:

1. **Start Backend**:
   ```bash
   cd backend
   source venv/bin/activate
   python app.py
   ```

2. **Open Browser** with Console (F12)

3. **Login**:
   - Go to `login.html`
   - Email: `admin@protechsolutions.cm`
   - Password: `admin_password`
   - Check console for: `"Login successful!"`

4. **Add to Cart**:
   - Go to `Products.html`
   - Click "Add to Cart" on a product
   - Check console for: `"Cart saved successfully"`

5. **View Cart**:
   - Go to `cart.html`
   - Verify items are displayed

6. **Checkout**:
   - Click "Proceed to Checkout"
   - **Watch console logs carefully**
   - Should see: `"✅ Order created successfully!"`

---

## 📞 Still Not Working?

If you've tried everything above and it still fails:

1. **Copy the ENTIRE console output** (all the logs)
2. **Copy the error message** from the alert
3. **Check the backend terminal** for any error messages
4. Look for these specific patterns in the logs

The enhanced logging will tell you exactly where the process is failing!

---

## 🎯 Expected Success Flow

```
User clicks "Proceed to Checkout"
  ↓
✓ Check ApiClient exists
  ↓
✓ Check user is logged in (has token)
  ↓
✓ Check cart has items
  ↓
✓ Prepare order data
  ↓
→ Send POST request to http://127.0.0.1:5000/api/orders/
  ↓
← Backend receives request
  ↓
← Backend validates JWT token
  ↓
← Backend fetches product prices from database
  ↓
← Backend creates Order in database
  ↓
← Backend creates OrderItems in database
  ↓
← Backend returns: {order_id: 1, total: 900000}
  ↓
✓ Frontend shows success alert
  ↓
✓ Cart is cleared
  ↓
✅ DONE!
```

---

**The new version has extensive logging. Just open the console and you'll see exactly where it's failing!** 🔍
