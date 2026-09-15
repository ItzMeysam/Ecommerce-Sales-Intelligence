import pandas as pd
import random


def generate_customers(n: int = 100) -> pd.DataFrame:
    data = []
    cities = ["Tehran", "Shiraz", "Isfahan", "Tabriz", "Mashhad"]

    for i in range(n):
        customer_id = f"C{101 + i}"
        city = random.choice(cities)
        age = random.randint(18, 65)
        is_premium = random.choice([True, False])
        dict1 = {
            "customer_id": customer_id,
            "is_premium": is_premium,
            "city": city,
            "age": age
        }
        data.append(dict1)
    df = pd.DataFrame(data)
    return df


def generate_orders(n: int = 500) -> pd.DataFrame:
    data = []
    statuses = ["Delivered", "Cancelled", "Returned"]
    for i in range(n):
        order_id = f"O{1001 + i}"
        customer_id = f"C{random.randint(101, 200)}"
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        order_date = f"2024-{month:02d}-{day:02d}"
        status = random.choice(statuses)

        dict2 = {
            "order_id": order_id,
            "customer_id": customer_id,
            "order_date": order_date,
            "status": status
        }
        data.append(dict2)
    df = pd.DataFrame(data)
    return df


def generate_order_items(n: int = 1200) -> pd.DataFrame:
    data = []
    categories = ["Electronics", "Clothing", "Home & Kitchen", "Books", "Beauty"]
    for i in range(n):
        item_id = f"I{10001 + i}"
        order_id = f"O{random.randint(1001, 1500)}"
        category = random.choice(categories)
        quantity = random.randint(1, 5)
        price = random.randint(10, 500)

        dict3 = {
            "item_id": item_id,
            "order_id": order_id,
            "category": category,
            "quantity": quantity,
            "price": price
        }
        data.append(dict3)
    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":
    customers_df = generate_customers(100)
    customers_df.to_csv("customers.csv", index=False)
    orders_df = generate_orders(500)
    orders_df.to_csv("orders.csv", index=False)
    items_df = generate_order_items(1200)
    items_df.to_csv("order_items.csv", index=False)
