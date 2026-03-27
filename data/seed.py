import sqlite3
import os

def seed_products():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/inventory.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        reorder_level INTEGER NOT NULL,
        description TEXT
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] > 0:
        print("Database already seeded.")
        conn.close()
        return

    products = [
        ("Heavy Duty Power Supply 220V", "Electronics", 45, 129.99, 10, "Industrial-grade 220V power supply, 500W output, compatible with heavy machinery"),
        ("Standard Power Supply 110V", "Electronics", 120, 59.99, 20, "Standard 110V power supply, 300W, for office equipment"),
        ("Industrial Motor 5HP", "Machinery", 8, 450.00, 5, "5 horsepower electric motor, 3-phase, 220V compatible"),
        ("Safety Helmet Type-A", "Safety", 200, 15.99, 50, "Hard hat type A, impact resistant, for warehouse use"),
        ("Safety Gloves Large", "Safety", 350, 4.99, 100, "Heavy duty rubber gloves, size large, chemical resistant"),
        ("Hydraulic Jack 10T", "Tools", 15, 189.99, 5, "10-ton hydraulic floor jack, heavy duty steel construction"),
        ("Conveyor Belt 10m", "Machinery", 3, 899.99, 2, "Industrial conveyor belt, 10 meters, rubber surface"),
        ("LED Warehouse Light", "Electrical", 75, 34.99, 20, "High-bay LED light, 150W, suitable for large warehouses"),
        ("Forklift Battery 48V", "Electronics", 6, 749.99, 3, "48V forklift replacement battery, 600Ah capacity"),
        ("Fire Extinguisher CO2", "Safety", 30, 89.99, 10, "CO2 fire extinguisher, 5kg, suitable for electrical fires"),
        ("Pallet Wrap 500m", "Packaging", 90, 19.99, 25, "Stretch pallet wrap, 500m roll, 23 micron thickness"),
        ("Industrial Fan 36inch", "Electrical", 12, 299.99, 4, "36-inch industrial ceiling fan, 3-speed, 220V"),
        ("Drill Bits Set HSS", "Tools", 55, 24.99, 15, "High-speed steel drill bits set, 19 pieces, 1-10mm"),
        ("Steel Shelving Unit", "Storage", 22, 159.99, 5, "Heavy duty steel shelving, 5 tiers, 400kg capacity"),
        ("Barcode Scanner USB", "Electronics", 18, 79.99, 5, "USB barcode scanner, compatible with all warehouse systems"),
    ]

    cursor.executemany("""
    INSERT INTO products (name, category, quantity, price, reorder_level, description)
    VALUES (?, ?, ?, ?, ?, ?)
    """, products)

    conn.commit()
    conn.close()
    print("Database seeded successfully.")

if __name__ == "__main__":
    seed_products()