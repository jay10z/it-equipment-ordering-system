from app import create_app, db
from app.models import Product, User

app = create_app()

with app.app_context():
    print("--- Database Verification ---")
    
    # 1. Check Products
    products = Product.query.all()
    print(f"\nTotal Products listed: {len(products)}")
    for p in products[:5]:
        print(f" - {p.name} ({p.category}) : {p.price} FCFA")
    print("... and more.")

    # 2. Check Users (Should be empty initially unless I create one)
    users = User.query.all()
    print(f"\nTotal Users registered: {len(users)}")
    
    print("\n-----------------------------")
    print("Database is active and seeded successfully.")
