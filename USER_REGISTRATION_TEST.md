# 🧪 Registration & Database Verification Guide

This guide will walk you through how to register a new user on the ProTech Solutions website and verify that their data is correctly stored in the MySQL database.

## 🟢 Part 1: Registering a New User (Frontend)

1.  **Start the Server** (if not already running):
    Open your terminal in `backend` and run:
    ```bash
    source venv/bin/activate
    python app.py
    ```

2.  **Open the Registration Page**:
    Open the file `src/register.html` in your web browser.

3.  **Fill out the Form**:
    Enter the following test details:
    *   **Full Name**: Jean Dupont
    *   **Email**: `jean.dupont@example.com`
    *   **Phone**: `699887766` (Valid Cameroon format)
    *   **Password**: `password123`

4.  **Submit**:
    Click the **"Register"** button.
    *   *Success Indicator*: You should see a green message "Registration successful! Please login." and be redirected to the login page.

---

## 🔵 Part 2: Verifying in the Database (3 Methods)

### Method A: Using the Admin Dashboard (Easiest)
1.  **Log in as Admin**:
    *   Go to `src/login.html`.
    *   Email: `admin@protechsolutions.cm`
    *   Password: `admin_password`
2.  **Go to Dashboard**:
    *   You should be redirected to `admin.html`.
3.  **Check Users Tab**:
    *   Click on the **"Users"** tab in the sidebar.
    *   **Verification**: You should see a row for **Jean Dupont** with ID, email, and "Customer" role.

### Method B: Using Python Script (Terminal)
I have included a script called `verify_db.py` in the backend folder.
1.  Open a new terminal window.
2.  Navigate to the backend:
    ```bash
    cd backend
    source venv/bin/activate
    ```
3.  Run the verification script:
    ```bash
    python verify_db.py
    ```
4.  **Output**: Look for the section "Total Users registered". It should increment (e.g., from 1 to 2) and list the new user.

### Method C: Using MySQL Command Line (Advanced)
1.  Open your terminal.
2.  Log into MySQL:
    ```bash
    mysql -u root -p protech_db
    ```
    (Press Enter if you have no password set for root).
3.  Run the query:
    ```sql
    SELECT * FROM user;
    ```
4.  **Result**: You will see the raw data table showing the new user entry.

---

## ❓ Troubleshooting

*   **"Failed to fetch"**: Ensure `python app.py` is running.
*   **"Email already registered"**: You tried to register `jean.dupont@example.com` twice. Try a different email.
*   **Database connection error**: Ensure MySQL server is running properly.
