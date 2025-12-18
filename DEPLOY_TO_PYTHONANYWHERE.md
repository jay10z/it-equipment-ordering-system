# Deploying to PythonAnywhere (Free MySQL Hosting)

This guide will help you deploy your Flask application with a MySQL database to PythonAnywhere for free.

## Prerequisites
- A GitHub account (recommended for easy code transfer) OR you can upload files manually.
- Your project files are ready.

## Step 1: Create a PythonAnywhere Account
1. Go to [www.pythonanywhere.com](https://www.pythonanywhere.com/).
2. Click **Pricing & Signup**.
3. Create a **Beginner** (Free) account.

## Step 2: Upload Your Code
The easiest way is to use a Bash console on PythonAnywhere to clone your code from GitHub. If you haven't pushed your code to GitHub yet, you can upload the zip file.

**Option A: Using GitHub (Recommended)**
1. On PythonAnywhere, go to the **Consoles** tab.
2. Click **Bash**.
3. Clone your repository:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git mysite
   ```
   *(Replace with your actual GitHub repo URL)*

**Option B: Uploading Zip**
1. Zip your project folder on your computer.
2. On PythonAnywhere, go to the **Files** tab.
3. Upload the zip file.
4. Open a **Bash** console and run:
   ```bash
   unzip yourfile.zip
   mv Clothing-Store-with-HTML-CSS-and-JS-master mysite
   ```

## Step 3: Create the MySQL Database
1. Go to the **Databases** tab.
2. under "Create a Database", enter a name (e.g., `protech_db`) and click **Create**.
3. Note down the **Database Host** address (usually something like `yourusername.mysql.pythonanywhere-services.com`).
4. Set a password for your database in the "Password" section if you haven't already.

## Step 4: Install Dependencies
In the Bash console, run:

```bash
cd mysite
# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r backend/requirements.txt
pip install python-dotenv
```

## Step 5: Configure the Web App
1. Go to the **Web** tab.
2. Click **Add a new web app**.
3. Click **Next**, select **Flask**, then select **Python 3.10** (or your version).
4. **Important**: For the path, just accept the default for now (we will change it).
5. Once created, look at the **Code** section on the Web tab.
   - **Source code**: Enter the path to your project, e.g., `/home/yourusername/mysite/backend`.
   - **Working directory**: Enter the same path, e.g., `/home/yourusername/mysite/backend`.
6. **Virtualenv**: Enter the path to your virtualenv: `/home/yourusername/mysite/venv`.

## Step 6: Configure the WSGI File
1. In the **Code** section of the Web tab, click the link to edit the **WSGI configuration file** (it looks like `/var/www/yourusername_pythonanywhere_com_wsgi.py`).
2. Delete everything and replace it with this:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/mysite/backend'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables
os.environ['SECRET_KEY'] = 'your-secret-key-here'
# Format: mysql+pymysql://username:password@hostname/databasename
os.environ['DATABASE_URL'] = 'mysql+pymysql://YOUR_USERNAME:YOUR_PASSWORD@YOUR_USERNAME.mysql.pythonanywhere-services.com/YOUR_USERNAME$protech_db'

from app import create_app
application = create_app()
```

*Replace `YOUR_USERNAME`, `YOUR_PASSWORD`, and check the database name matching exactly what is in the Databases tab.*

## Step 7: Initialize the Database
Go back to the **Bash** console:

```bash
# Sourcing the venv again if needed
source venv/bin/activate
cd mysite/backend

# Set the DB URL temporarily for the command line ops
export DATABASE_URL='mysql+pymysql://YOUR_USERNAME:YOUR_PASSWORD@YOUR_USERNAME.mysql.pythonanywhere-services.com/YOUR_USERNAME$protech_db'

# Run migrations
flask db upgrade

# Seed database
python seed.py
```

## Step 8: Reload and Visit
1. Go back to the **Web** tab.
2. Click the big green **Reload** button.
3. Click the link to your site (e.g., `https://yourusername.pythonanywhere.com`).
