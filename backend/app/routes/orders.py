from flask import Blueprint, jsonify, request
from app import db
from app.models import Order, OrderItem, Product, User
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('orders', __name__)

def is_admin():
    """Helper function to check if current user is admin"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        return user and user.is_admin
    except:
        return False

@bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    """Create a new order from cart items with STOCK CHECK"""
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data or 'items' not in data:
        return jsonify({'message': 'No items provided'}), 400
    
    cart_items = data['items']
    if not cart_items or len(cart_items) == 0:
        return jsonify({'message': 'Cart is empty'}), 400
    
    try:
        total_amount = 0
        order_items_data = []
        products_to_update = []
        
        # VALIDATION PHASE
        for item in cart_items:
            if 'id' not in item or 'quantity' not in item:
                continue
                
            product = Product.query.get(item['id'])
            if not product:
                return jsonify({'message': f'Product with ID {item["id"]} not found'}), 404
            
            quantity = int(item['quantity'])
            if quantity <= 0:
                continue
                
            # Check Stock
            if product.stock < quantity:
                return jsonify({
                    'message': f'Insufficient stock for {product.name}. Only {product.stock} left.'
                }), 400
            
            item_total = float(product.price) * quantity
            total_amount += item_total
            
            order_items_data.append({
                'product_id': product.id,
                'product_name': product.name,
                'quantity': quantity,
                'price': float(product.price)
            })
            products_to_update.append((product, quantity))
        
        if len(order_items_data) == 0:
            return jsonify({'message': 'No valid items in cart'}), 400
        
        # EXECUTION PHASE
        new_order = Order(
            user_id=current_user_id,
            total_amount=total_amount,
            status='Pending'
        )
        db.session.add(new_order)
        db.session.flush()
        
        # Create items and deduct stock
        for item_data in order_items_data:
            order_item = OrderItem(order_id=new_order.id, **item_data)
            db.session.add(order_item)
            
        for product, quantity in products_to_update:
            product.stock -= quantity
            product.update_availability() # Update "In Stock" label
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order placed successfully',
            'order_id': new_order.id,
            'total': total_amount
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to create order: {str(e)}'}), 500

@bp.route('/my-orders', methods=['GET'])
@jwt_required()
def get_my_orders():
    """Get orders for the current user"""
    current_user_id = int(get_jwt_identity())
    orders = Order.query.filter_by(user_id=current_user_id).order_by(Order.created_at.desc()).all()
    return jsonify([o.to_dict() for o in orders]), 200

@bp.route('/', methods=['GET'])
@jwt_required()
def get_all_orders():
    """Get all orders (Admin only)"""
    if not is_admin():
        return jsonify({'message': 'Admin access required'}), 403
        
    orders = Order.query.order_by(Order.created_at.desc()).all()
    # Enrich with user details for admin view
    result = []
    for o in orders:
        data = o.to_dict()
        user = User.query.get(o.user_id)
        data['user_email'] = user.email if user else 'Unknown'
        data['user_name'] = user.full_name if user else 'Unknown'
        result.append(data)
        
    return jsonify(result), 200

@bp.route('/<int:id>/status', methods=['PATCH'])
@jwt_required()
def update_order_status(id):
    """Update order status (Admin only)"""
    if not is_admin():
        return jsonify({'message': 'Admin access required'}), 403
    
    data = request.get_json()
    status = data.get('status')
    
    allowed_statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']
    if status not in allowed_statuses:
        return jsonify({'message': f'Invalid status. Allowed: {allowed_statuses}'}), 400
        
    order = Order.query.get_or_404(id)
    order.status = status
    db.session.commit()
    
    return jsonify({'message': f'Order status updated to {status}', 'order': order.to_dict()}), 200
