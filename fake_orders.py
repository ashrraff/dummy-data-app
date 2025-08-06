import requests
from faker import Faker
import random
import time


fake = Faker()

API_URL = "http://localhost:8000"

def create_customer():
    data = {
        "name": fake.name(),
        "email": fake.unique.email(),
        "region": fake.state()
    }

    response = requests.post(f"{API_URL}/customers", json=data)
    if response.status_code == 200:
        print(f"[Customer created] {data['email']}")
    else:
        print(f"[Customer Failed] {response.text}")

def get_customer_ids():
    response = requests.get(f"{API_URL}/customers")
    if response.status_code == 200:
        response_data = response.json()
        cids = [item["id"] for item in response_data]
        print(f"{len(cids)} CIDs Returned")
        return cids
    else:
        print(f"CIDs failed")
        return None


def create_sale(customer_id, product_id):
    data = {
        "customer_id": customer_id,
        "product_id": product_id,
        "quantity": random.randint(1,10)
    }

    response = requests.post(f"{API_URL}/sales", json=data)
    if response.status_code == 200:
        print(f"[Sale Created] cust: {customer_id} prod: {product_id}")
    else:
        print(f"[Sale Failed] {response.text}")


def create_product():
    data = {
        "name": fake.unique.word().capitalize(),
        "category": fake.random_element(elements=["Electronics", "Books", "Clothing", "Toys", "Groceries"]),
        "price": round(fake.pyfloat(left_digits=2, right_digits=2, positive=True, min_value=1.0), 2)
    }

    response = requests.post(f"{API_URL}/products", json=data)

    if response.status_code == 200:
        print(f"[Product created] {data['name']} - ${data['price']}")
    else:
        print(f"[Product Failed] {response.status_code} - {response.text}")

def get_product_ids():
    response = requests.get(f"{API_URL}/products")
    if response.status_code == 200:
        response_data = response.json()
        pids = [item["id"] for item in response_data]
        print(f"{len(pids)} PIDs Returned")
        return pids
    else:
        print(f"PIDs failed")
        return None


def main():

    for _ in range(70):

        # create_product()

        customer_choice = random.randint(1,5)

        if customer_choice == 3:
            create_customer()
        else:
            pass

        cids = get_customer_ids()
        pids = get_product_ids()

        customer_id = random.choice(cids)
        product_id = random.choice(pids)
        create_sale(customer_id, product_id)

        time.sleep(2)
    
if __name__ == "__main__":
    main()




