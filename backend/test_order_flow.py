#!/usr/bin/env python3
"""
Test script to verify the complete checkout-to-order flow
"""

from app import create_app, db
from app.models import User, Product, Order, OrderItem
import json

app = create_app()

def test_order_creation():
    with app.app_context():
        print("=" * 60)
        print("TESTING CHECKOUT-TO-ORDER FLOW")
        print("=" * 60)
        
        # 1. Check if we have products
        products = Product.query.all()
        print(f"\n✓ Products in database: {len(products)}")
        if len(products) > 0:
            print(f"  Sample: {products[0].name} - {products[0].price} FCFA")
        
        # 2. Check if we have users
        users = User.query.all()
        print(f"\n✓ Users in database: {len(users)}")
        for user in users:
            print(f"  - {user.full_name} ({user.email}) - Admin: {user.is_admin}")
        
        # 3. Check existing orders
        orders = Order.query.all()
        print(f"\n✓ Existing orders: {len(orders)}")
        for order in orders:
            print(f"  Order #{order.id}: User {order.user_id}, Total: {order.total_amount} FCFA, Status: {order.status}")
            items = OrderItem.query.filter_by(order_id=order.id).all()
            for item in items:
                print(f"    - {item.product_name} x{item.quantity} @ {item.price} FCFA")
        
        # 4. Simulate order creation (like the API would do)
        print("\n" + "=" * 60)
        print("SIMULATING ORDER CREATION")
        print("=" * 60)
        
        # Find a non-admin user (or create one)
        customer = User.query.filter_by(is_admin=False).first()
        if not customer:
            print("\n⚠ No customer user found. Creating test customer...")
            customer = User(
                full_name="Test Customer",
                email="test@customer.com",
                phone="677000000",
                is_admin=False
            )
            customer.set_password("test123")
            db.session.add(customer)
            db.session.commit()
            print(f"✓ Created customer: {customer.email}")
        
        # Simulate cart items
        cart_items = [
            {"id": 1, "quantity": 2},
            {"id": 5, "quantity": 1}
        ]
        
        print(f"\n📦 Simulating cart with {len(cart_items)} items for user: {customer.email}")
        
        # Create order
        total_amount = 0
        new_order = Order(user_id=customer.id, status='Pending')
        db.session.add(new_order)
        db.session.flush()
        
        order_items_objects = []
        
        for item in cart_items:
            product = Product.query.get(item['id'])
            if not product:
                print(f"  ⚠ Product ID {item['id']} not found, skipping...")
                continue
            
            item_total = product.price * item['quantity']
            total_amount += item_total
            
            print(f"  + {product.name} x{item['quantity']} = {item_total:,.0f} FCFA")
            
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                product_name=product.name,
                quantity=item['quantity'],
                price=product.price
            )
            order_items_objects.append(order_item)
        
        new_order.total_amount = total_amount
        db.session.add_all(order_items_objects)
        db.session.commit()
        
        print(f"\n✅ ORDER CREATED SUCCESSFULLY!")
        print(f"   Order ID: #{new_order.id}")
        print(f"   Total: {total_amount:,.0f} FCFA")
        print(f"   Items: {len(order_items_objects)}")
        
        # 5. Verify order was saved
        print("\n" + "=" * 60)
        print("VERIFICATION")
        print("=" * 60)
        
        saved_order = Order.query.get(new_order.id)
        if saved_order:
            print(f"\n✓ Order #{saved_order.id} found in database")
            print(f"  User ID: {saved_order.user_id}")
            print(f"  Total: {saved_order.total_amount} FCFA")
            print(f"  Status: {saved_order.status}")
            print(f"  Created: {saved_order.created_at}")
            
            items = OrderItem.query.filter_by(order_id=saved_order.id).all()
            print(f"\n  Order Items ({len(items)}):")
            for item in items:
                print(f"    - {item.product_name} x{item.quantity} @ {item.price} FCFA")
        else:
            print("\n❌ Order not found in database!")
        
        print("\n" + "=" * 60)
        print("TEST COMPLETE")
        print("=" * 60)

if __name__ == '__main__':
    test_order_creation()
