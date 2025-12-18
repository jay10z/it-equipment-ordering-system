import os
from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
cors = CORS()

def create_app(config_class=Config):
    # Determine directories for frontend and images
    app_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(app_dir)
    project_root = os.path.dirname(backend_dir)
    
    frontend_dir = os.path.join(project_root, 'src')
    image_dir = os.path.join(project_root, 'images')

    # Initialize Flask with the frontend directory as the static folder
    app = Flask(__name__, 
                static_folder=frontend_dir, 
                static_url_path='')
    
    app.config.from_object(config_class)
    
    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)

    # 🔹 Route to serve the main website (index.html)
    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, 'index.html')

    # 🔹 Root health check route (moved to /api/health)
    @app.route("/api/health")
    def health():
        return jsonify({
            "status": "OK",
            "message": "Backend API is running"
        }), 200

    # 🔹 Route to serve images from the root 'images' folder
    @app.route('/images/<path:filename>')
    def serve_images(filename):
        return send_from_directory(image_dir, filename)

    # Register Blueprints
    from app.routes.auth import bp as auth_bp
    from app.routes.products import bp as products_bp
    from app.routes.orders import bp as orders_bp

    from app.routes.users import bp as users_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(users_bp, url_prefix='/api/users')

    return app

