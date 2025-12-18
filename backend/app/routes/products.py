from flask import Blueprint, jsonify, request
from app import db
from app.models import Product, User
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('products', __name__)

def is_admin():
    """Helper function to check if current user is admin"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        return user and user.is_admin
    except:
        return False

@bp.route('/', methods=['GET'])
def get_products():
    """Get all products"""
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products]), 200

@bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    """Get single product by ID"""
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict()), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    """Create new product (Admin only)"""
    if not is_admin():
        return jsonify({'message': 'Admin access required'}), 403
    
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('name') or not data.get('category') or not data.get('price'):
        return jsonify({'message': 'Missing required fields: name, category, price'}), 400
    
    try:
        new_product = Product(
            name=data['name'],
            category=data['category'],
            price=float(data['price']),
            description=data.get('description', ''),
            specs=data.get('specs', ''),
            image_url=data.get('image_url'),
            stock=int(data.get('stock', 0)),
            availability=data.get('availability', 'In Stock'),
            warranty=data.get('warranty', '')
        )
        new_product.update_availability()
        
        db.session.add(new_product)
        db.session.commit()
        
        return jsonify({
            'message': 'Product created successfully',
            'product': new_product.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to create product: {str(e)}'}), 500

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    """Update product (Admin only)"""
    if not is_admin():
        return jsonify({'message': 'Admin access required'}), 403
    
    product = Product.query.get_or_404(id)
    data = request.get_json()
    
    try:
        # Update fields if provided
        if 'name' in data:
            product.name = data['name']
        if 'category' in data:
            product.category = data['category']
        if 'price' in data:
            product.price = float(data['price'])
        if 'description' in data:
            product.description = data['description']
        if 'specs' in data:
            product.specs = data['specs']
        if 'image_url' in data:
            product.image_url = data['image_url']
        if 'stock' in data:
            product.stock = int(data['stock'])
        if 'availability' in data:
            product.availability = data['availability']
        if 'warranty' in data:
            product.warranty = data['warranty']
        if 'stock' in data or 'availability' not in data:
            product.update_availability()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Product updated successfully',
            'product': product.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to update product: {str(e)}'}), 500

@bp.route('/<int:id>/stock', methods=['PATCH'])
@jwt_required()
def update_stock(id):
    """Update product stock (Admin only)"""
    if not is_admin():
        return jsonify({'message': 'Admin access required'}), 403
    
    product = Product.query.get_or_404(id)
    data = request.get_json()
    
    if 'stock' not in data:
        return jsonify({'message': 'Stock value required'}), 400
    
    try:
        product.stock = int(data['stock'])
        
        product.update_availability()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Stock updated successfully',
            'product': product.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to update stock: {str(e)}'}), 500

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    """Delete product (Admin only)"""
    if not is_admin():
        return jsonify({'message': 'Admin access required'}), 403
    
    product = Product.query.get_or_404(id)
    
    try:
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to delete product: {str(e)}'}), 500
