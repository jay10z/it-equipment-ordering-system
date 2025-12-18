from app import create_app, db
from app.models import User

app = create_app()

def create_admin_user():
    with app.app_context():
        email = "admin@protechsolutions.cm"
        password = "admin_password"
        
        # Check if exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"Admin user {email} already exists.")
            # Update to admin just in case
            existing_user.is_admin = True
            existing_user.set_password(password)
            db.session.commit()
            print("Updated existing user to be Admin with new password.")
        else:
            new_admin = User(
                full_name="System Administrator",
                email=email,
                phone="600000000",
                is_admin=True
            )
            new_admin.set_password(password)
            db.session.add(new_admin)
            db.session.commit()
            print(f"Created new Admin user: {email}")

if __name__ == "__main__":
    create_admin_user()
