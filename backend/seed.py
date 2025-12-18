from app import create_app, db
from app.models import Product

app = create_app()

def seed_products():
    products = [
        {
            "name": "Dell Latitude 5420",
            "category": "Computers",
            "price": 450000,
            "specs": """14" FHD, Intel i5-1135G7, 8GB RAM, 256GB SSD""",
            "availability": "In Stock",
            "warranty": "12 months",
            "image_url": "images/dell_latitude_5420.png",
            "stock": 50
        },
        {
            "name": "HP ProBook 450 G8",
            "category": "Computers",
            "price": 520000,
            "specs": """15.6" FHD, Intel i7-1165G7, 16GB RAM, 512GB SSD""",
            "availability": "In Stock",
            "warranty": "12 months",
            "image_url": "images/hp_probook_450_g8.png",
            "stock": 50
        },
        {
            "name": "Lenovo ThinkPad T14",
            "category": "Computers",
            "price": 480000,
            "specs": """14" FHD, AMD Ryzen 5, 8GB RAM, 256GB SSD""",
            "availability": "In Stock",
            "warranty": "12 months",
            "image_url": "images/dell_latitude_5420.png",
            "stock": 50
        },
        {
            "name": "Cisco Small Business Router",
            "category": "Networking",
            "price": 95000,
            "specs": "Dual-band, 5 Gigabit ports, VPN support",
            "availability": "In Stock",
            "warranty": "24 months",
            "image_url": "images/cisco_router.png",
            "stock": 50
        },
        {
            "name": "TP-Link 24-Port Switch",
            "category": "Networking",
            "price": 120000,
            "specs": "10/100/1000 Mbps, Rackmount, Unmanaged",
            "availability": "In Stock",
            "warranty": "36 months",
            "image_url": "images/cisco_router.png",
            "stock": 50
        },
        {
            "name": "Ubiquiti UniFi AP AC Pro",
            "category": "Networking",
            "price": 85000,
            "specs": "Dual-band WiFi, PoE, up to 450 Mbps",
            "availability": "In Stock",
            "warranty": "12 months",
            "image_url": "images/cisco_router.png",
            "stock": 50
        },
        {
            "name": "Logitech MX Master 3",
            "category": "Accessories",
            "price": 35000,
            "specs": "Wireless Mouse, 7 buttons, 4000 DPI",
            "availability": "In Stock",
            "warranty": "12 months",
            "image_url": "images/logitech_mx_master_3.png",
            "stock": 50
        },
        {
            "name": "Logitech MX Keys",
            "category": "Accessories",
            "price": 45000,
            "specs": "Wireless Keyboard, Backlit, USB-C charging",
            "availability": "In Stock",
            "warranty": "12 months",
            "image_url": "images/logitech_mx_master_3.png",
            "stock": 50
        },
        {
            "name": "HDMI Cable 2m",
            "category": "Accessories",
            "price": 3500,
            "specs": "4K support, High speed, Gold plated",
            "availability": "In Stock",
            "warranty": "6 months",
            "image_url": "images/logitech_mx_master_3.png",
            "stock": 50
        },
        {
            "name": "Seagate Backup Plus 2TB",
            "category": "Storage",
            "price": 45000,
            "specs": "External HDD, USB 3.0, Portable",
            "availability": "In Stock",
            "warranty": "24 months",
            "image_url": "images/hp_probook_450_g8.png",
            "stock": 50
        },
        {
            "name": "Samsung T7 SSD 1TB",
            "category": "Storage",
            "price": 95000,
            "specs": "External SSD, USB 3.2, 1050 MB/s read",
            "availability": "In Stock",
            "warranty": "36 months",
            "image_url": "images/hp_probook_450_g8.png",
            "stock": 50
        },
        {
            "name": "SanDisk Ultra 128GB USB",
            "category": "Storage",
            "price": 7500,
            "specs": "USB 3.0, 130 MB/s read speed",
            "availability": "In Stock",
            "warranty": "12 months",
            "image_url": "images/hp_probook_450_g8.png",
            "stock": 50
        }
    ]

    print("Seeding products...")
    for p_data in products:
        if not Product.query.filter_by(name=p_data['name']).first():
            product = Product(**p_data)
            db.session.add(product)
    
    db.session.commit()
    print("Products seeded!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Ensure tables exist
        seed_products()
