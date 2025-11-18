import pandas as pd
import random
from datetime import datetime, timedelta

# Number of rows you want
N = 5000

products = [
    ("P001", "Wireless Earphones", "boAt", "Electronics", "Audio"),
    ("P002", "Bluetooth Speaker", "JBL", "Electronics", "Audio"),
    ("P003", "Smart Watch", "Noise", "Electronics", "Wearable"),
    ("P004", "Power Bank", "Mi", "Electronics", "Accessories"),
    ("P005", "Laptop Bag", "Dell", "Accessories", "Bags"),
    ("P006", "Running Shoes", "Nike", "Fashion", "Footwear"),
    ("P007", "Water Bottle", "Decathlon", "Fitness", "Accessories"),
    ("P008", "Office Chair", "GreenSoul", "Furniture", "Office"),
    ("P009", "LED Monitor", "Samsung", "Electronics", "Display"),
    ("P010", "Keyboard Mouse Combo", "Logitech", "Electronics", "Accessories"),
]

cities = {
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik"],
    "Karnataka": ["Bengaluru", "Mysuru"],
    "Delhi": ["New Delhi"],
    "Tamil Nadu": ["Chennai", "Coimbatore"],
    "West Bengal": ["Kolkata"],
    "Uttar Pradesh": ["Lucknow", "Noida"],
}

sales_channels = ["Amazon", "Flipkart", "Meesho", "JioMart", "Website"]
payment_methods = ["UPI", "Paytm", "PhonePe", "Credit Card", "Debit Card", "Cash on Delivery"]

rows = []

start_date = datetime(2025, 1, 1)

for i in range(N):
    order_id = f"O{i}"
    product_id, product_name, brand, category, subcat = random.choice(products)

    price = round(random.uniform(300, 5000), 2)
    qty = random.randint(1, 4)
    revenue = price * qty

    discount_percent = random.randint(5, 40)
    discount_amount = round(revenue * (discount_percent / 100), 2)

    final_revenue = round(revenue - discount_amount, 2)

    state = random.choice(list(cities.keys()))
    city = random.choice(cities[state])

    customer_id = f"CUST{random.randint(1000,9999)}"
    customer_name = f"Customer_{random.randint(1,9999)}"

    order_date = start_date + timedelta(days=random.randint(0, 364))

    rows.append([
        order_id, order_date.date(), product_id, product_name, category,
        brand, subcat, price, qty, revenue, discount_percent, discount_amount,
        final_revenue, customer_id, customer_name, city, state,
        random.choice(["North", "South", "East", "West", "Central"]),
        random.choice(sales_channels),
        random.choice(payment_methods)
    ])

df = pd.DataFrame(rows, columns=[
    "OrderID", "OrderDate", "ProductID", "ProductName", "Category", "Brand",
    "SubCategory", "Price", "Quantity", "Revenue", "DiscountPercent",
    "DiscountAmount", "FinalRevenue", "CustomerID", "CustomerName",
    "City", "State", "Region", "SalesChannel", "PaymentMethod"
])

df.to_csv("/Users/chandrakprajapati/Desktop/FUTURE_DS_01/dataset/dataset.csv", index=False)

print("✅ Professional 5000-row dataset generated successfully!")