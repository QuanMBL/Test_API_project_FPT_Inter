#!/usr/bin/env python3
"""
Script to generate API data for monitoring
"""
import requests
import time
import random
import threading

def make_request(url, endpoint, method="GET", data=None):
    """Make HTTP request to API"""
    try:
        if method == "GET":
            response = requests.get(f"{url}{endpoint}", timeout=5)
        elif method == "POST":
            response = requests.post(f"{url}{endpoint}", json=data, timeout=5)
        
        print(f"✅ {method} {url}{endpoint} - Status: {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"❌ Error calling {url}{endpoint}: {e}")
        return None

def generate_user_data():
    """Generate random user data"""
    return {
        "name": f"User {random.randint(1, 1000)}",
        "email": f"user{random.randint(1, 1000)}@example.com",
        "age": random.randint(18, 80)
    }

def generate_product_data():
    """Generate random product data"""
    return {
        "name": f"Product {random.randint(1, 1000)}",
        "price": round(random.uniform(10, 1000), 2),
        "description": f"Description for product {random.randint(1, 1000)}"
    }

def generate_order_data():
    """Generate random order data"""
    return {
        "user_id": random.randint(1, 100),
        "product_id": random.randint(1, 100),
        "quantity": random.randint(1, 10),
        "total": round(random.uniform(50, 500), 2)
    }

def generate_payment_data():
    """Generate random payment data"""
    return {
        "order_id": random.randint(1, 100),
        "amount": round(random.uniform(10, 1000), 2),
        "method": random.choice(["credit_card", "debit_card", "paypal"])
    }

def api_worker(api_name, base_url, endpoints, data_generator=None):
    """Worker function to continuously call API endpoints"""
    print(f"🚀 Starting {api_name} worker...")
    
    while True:
        try:
            # Call different endpoints
            for endpoint in endpoints:
                if data_generator and endpoint != "/":
                    # POST request with data
                    make_request(base_url, endpoint, "POST", data_generator())
                else:
                    # GET request
                    make_request(base_url, endpoint)
                
                # Random delay between requests
                time.sleep(random.uniform(0.5, 2.0))
                
        except KeyboardInterrupt:
            print(f"🛑 Stopping {api_name} worker...")
            break
        except Exception as e:
            print(f"❌ Error in {api_name} worker: {e}")
            time.sleep(5)

def main():
    """Main function to start all API workers"""
    print("🎯 Starting API Data Generator...")
    print("This will generate continuous API requests to create monitoring data")
    print("Press Ctrl+C to stop")
    
    # API configurations
    apis = [
        {
            "name": "User API",
            "base_url": "http://localhost:8000",
            "endpoints": ["/api/users/", "/api/users/"],
            "data_generator": generate_user_data
        },
        {
            "name": "Product API", 
            "base_url": "http://localhost:8001",
            "endpoints": ["/api/products/", "/api/products/"],
            "data_generator": generate_product_data
        },
        {
            "name": "Order API",
            "base_url": "http://localhost:8002", 
            "endpoints": ["/api/orders/", "/api/orders/"],
            "data_generator": generate_order_data
        },
        {
            "name": "Payment API",
            "base_url": "http://localhost:8003",
            "endpoints": ["/api/payments/", "/api/payments/"],
            "data_generator": generate_payment_data
        }
    ]
    
    # Start worker threads for each API
    threads = []
    for api in apis:
        thread = threading.Thread(
            target=api_worker,
            args=(api["name"], api["base_url"], api["endpoints"], api["data_generator"])
        )
        thread.daemon = True
        thread.start()
        threads.append(thread)
        time.sleep(1)  # Stagger thread starts
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping all workers...")
        print("✅ API data generation stopped")

if __name__ == "__main__":
    main()
