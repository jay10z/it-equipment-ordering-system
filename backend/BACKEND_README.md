# ProTech Solutions - Backend Guide

## 🛠️ Setup & Installation

The backend is built with Python and Flask. Follow these steps to get it running.

### 1. Prerequisites
- Python 3.8+ installed
- Virtualenv (recommended)

### 2. Installation
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Database Initialization
1. Initialize the database schema:
   ```bash
   export FLASK_APP=app.py
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

2. Seed the database with sample products:
   ```bash
   python seed.py
   ```
   *This will populate the database with the 12 IT products used in the frontend.*

### 4. Running the Server
Start the development server:
```bash
python app.py
```
*The server will start at `http://127.0.0.1:5000`*

---

## 🔗 API Endpoints

### Authentication
- `POST /api/auth/register`
  - Body: `{ "email": "user@example.com", "password": "password", "full_name": "John Doe", "phone": "612345678" }`
- `POST /api/auth/login`
  - Body: `{ "email": "user@example.com", "password": "password" }`
  - Returns: `{ "access_token": "..." }`

### Products
- `GET /api/products` - Get all products
- `GET /api/products/<id>` - Get single product
- `POST /api/products` - Create product (Admin only)

---

##  frontend Integration

The frontend has been updated to automatically try connecting to this backend.
- `src/scripts/api.js` handles the communication.
- If the backend is **OFF**, the frontend uses "Fallback Mode" (hardcoded simulation).
- If the backend is **ON**, the frontend fetches real data and performs real authentication.

### How to Verify Intregration
1. Start the backend server (`python app.py`).
2. Open `src/index.html`.
3. Open Developer Tools (F12) -> Console.
4. You should see: `"Fetching products from API..."` followed by `"Products loaded from API"`.
