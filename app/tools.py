import sqlite3
from rag import retrieve_products

DB_PATH = "data/inventory.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def check_stock(product_name: str) -> str:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, category, quantity, price, reorder_level 
        FROM products 
        WHERE LOWER(name) LIKE LOWER(?)
    """, (f"%{product_name}%",))
    
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return f"No product found matching '{product_name}'. Try using semantic_search to find it."

    result = []
    for row in rows:
        name = row[0]
        category = row[1]
        quantity = row[2]
        price = row[3]
        reorder_level = row[4]
        status = "LOW STOCK - REORDER NEEDED" if quantity <= reorder_level else "OK"
        result.append(
            f"Product: {name}\n"
            f"Category: {category}\n"
            f"Quantity: {quantity} units\n"
            f"Price: ${price:.2f}\n"
            f"Reorder Level: {reorder_level} units\n"
            f"Status: {status}"
        )
    return "\n\n".join(result)


def update_inventory(product_name: str, quantity_change: int) -> str:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, quantity, reorder_level 
        FROM products 
        WHERE LOWER(name) LIKE LOWER(?)
    """, (f"%{product_name}%",))

    row = cursor.fetchone()
    if not row:
        conn.close()
        return f"No product found matching '{product_name}'"
    
    pid, name, current_qty, reorder_level = row
    new_qty = current_qty + quantity_change

    if new_qty < 0:
        conn.close()
        return f"Cannot update. This would result in negative stock ({new_qty}) for '{name}'."
    
    cursor.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_qty, pid))
    conn.commit()
    conn.close()

    action = "Added" if quantity_change > 0 else "Removed"
    status = "LOW STOCK - REORDER NEEDED" if new_qty <= reorder_level else "OK"

    return (
        f"{action} {abs(quantity_change)} units for '{name}'.\n"
        f"Previous quantity: {current_qty}\n"
        f"New quantity: {new_qty}\n"
        f"Status: {status}"
    )

def generate_report() -> str:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(quantity * price) FROM products")
    total_value = cursor.fetchone()[0]

    cursor.execute("""
        SELECT name, quantity, reorder_level 
        FROM products 
        WHERE quantity <= reorder_level
    """)
    low_stock = cursor.fetchall()

    cursor.execute("""
        SELECT category, SUM(quantity) as total
        FROM products
        GROUP BY category
        ORDER BY total DESC
    """)
    by_category = cursor.fetchall()
    conn.close()

    report = [
        "===== INVENTORY REPORT =====",
        f"Total Products: {total_products}",
        f"Total Inventory Value: ${total_value:,.2f}",
        "",
        "--- Stock by Category ---",
    ]
    for cat, qty in by_category:
        report.append(f"  {cat}: {qty} units")
    
    report.append("")
    if low_stock:
        report.append(f"--- Low Stock Alerts ({len(low_stock)} items) ---")
        for name, qty, reorder in low_stock:
            report.append(f"  {name}: {qty} units (reorder at {reorder})")
    else:
        report.append("--- No Low Stock Alerts ---")

    return "\n".join(report)

def semantic_search(query: str) -> str:
    return retrieve_products(query, top_k=3)