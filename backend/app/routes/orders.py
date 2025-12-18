from flask import Blueprint, jsonify, request
from app import db
from app.models import Order, OrderItem, Product
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('orders', __name__)

@bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    """Create a new order from cart items"""
    current_user_id = int(get_jwt_identity())  # Ensure it's an integer
    data = request.get_json()
    
    # Validate request
    if not data or 'items' not in data:
        return jsonify({'message': 'No items provided'}), 400
    
    cart_items = data['items']
    if not cart_items or len(cart_items) == 0:
        return jsonify({'message': 'Cart is empty'}), 400
    
    try:
        # Step 1: Calculate total and prepare order items FIRST
        total_amount = 0
        order_items_data = []
        
        for item in cart_items:
            # Validate item structure
            if 'id' not in item or 'quantity' not in item:
                continue
                
            # Get product from database
            product = Product.query.get(item['id'])
            if not product:
                return jsonify({'message': f'Product with ID {item["id"]} not found'}), 404
            
            # Validate quantity
            quantity = int(item['quantity'])
            if quantity <= 0:
                continue
            
            # Calculate item total using SERVER-SIDE price (security!)
            item_total = float(product.price) * quantity
            total_amount += item_total
            
            # Store item data for later
            order_items_data.append({
                'product_id': product.id,
                'product_name': product.name,
                'quantity': quantity,
                'price': float(product.price)
            })
        
        # Validate we have items
        if len(order_items_data) == 0:
            return jsonify({'message': 'No valid items in cart'}), 400
        
        # Step 2: Create Order with total_amount already set
        new_order = Order(
            user_id=current_user_id,
            total_amount=total_amount,
            status='Pending'
        )
        db.session.add(new_order)
        db.session.flush()  # Get the order ID
        
        # Step 3: Create OrderItems
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=new_order.id,
                **item_data
            )
            db.session.add(order_item)
        
        # Step 4: Commit transaction
        db.session.commit()
        
        return jsonify({
            'message': 'Order placed successfully',
            'order_id': new_order.id,
            'total': total_amount,
            'items_count': len(order_items_data)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Order creation error: {str(e)}")  # Server-side logging
        return jsonify({'message': f'Failed to create order: {str(e)}'}), 500

@bp.route('/', methods=['GET'])
# @jwt_required() # Admin only?
def get_orders():
    orders = Order.query.all()
    return jsonify([o.to_dict() for o in orders]), 200
