# Backend Implementation Plan

## 1. Architecture Overview
We will use a standard Flask factory pattern with Blueprints for modularity.
- **Database**: SQLite (easy setup), transferable to PostgreSQL.
- **Auth**: JWT (JSON Web Tokens) for stateless, secure authentication.
- **Security**: Bcrypt for password hashing, CORS protection, Input sanitization.

## 2. Directory Structure
```
backend/
├── app.py                  # Application entry point
├── config.py               # Configuration (Secret keys, DB URL)
├── requirements.txt        # Dependencies
└── app/
    ├── __init__.py         # App factory & extension initialization
    ├── models.py           # Database models (User, Product, Order)
    ├── utils/
    │   └── security.py     # Helper functions
    └── routes/
        ├── auth.py         # Login/Register endpoints
        ├── products.py     # Product management endpoints
        └── orders.py       # Order processing endpoints
```

## 3. Key Features Implementation

### Authentication (JWT)
- **Register**: Hash password with Bcrypt, save user.
- **Login**: Verify hash, generate Access Token (expires in 1 hour) and Refresh Token.
- **Protection**: Use `@jwt_required()` decorator on private routes (e.g., checkouts).

### Database Models
- **User**: `id`, `email`, `password_hash`, `is_admin`
- **Product**: `id`, `name`, `price`, `stock`, `category`
- **Order**: `id`, `user_id`, `total_amount`, `status`

## 4. Frontend Integration Steps
1. **API Client**: Create `api.js` to handle fetch requests with Authorization headers.
2. **Auth Flow**: Update `login.html` to store the received JWT in `localStorage`.
3. **Dynamic Data**: Replace `products.js` hardcoded array with a `fetch()` call to the backend.
