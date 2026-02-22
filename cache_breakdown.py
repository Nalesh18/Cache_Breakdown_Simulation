# What this program does:
    # 1. Creates a database
    # 2. Creates an in-memory cache with TTL
    # 3. Simulates cache expiry
    # 4. Simulates multiple users hitting system
    # 5. Shows cache breakdown
    # 6. Then fixes using mutex lock

import time
import threading

# Database
class Database:
    def fetch(self, key):
        print("Fetching from DB")
        time.sleep(1)
        return "Hot product data"

# Cache with TTL
class Cache:
    def __init__(self):
        self.data = {}
        self.expiry = {}

    def get(self, key):
        if key in self.data and time.time() < self.expiry[key]:
            return self.data[key]
        return None

    def set(self, key, value, ttl=3):
        self.data[key] = value
        self.expiry[key] = time.time() + ttl


# Service without protection
class ProductService:
    def __init__(self):
        self.cache = Cache()
        self.db = Database()

    def get_product(self, key):
        value = self.cache.get(key)

        if value:
            print("Cache hit")
            return value

        print("Cache miss")
        value = self.db.fetch(key)
        self.cache.set(key, value)
        return value


# Service with Mutex Lock
class SafeProductService(ProductService):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()

    def get_product(self, key):
        value = self.cache.get(key)
        if value:
            print("Cache hit")
            return value

        with self.lock:
            value = self.cache.get(key)
            if value:
                print("Cache hit after lock")
                return value

            print("Cache miss (safe)")
            value = self.db.fetch(key)
            self.cache.set(key, value)
            return value


# Simulation Functions
def simulate_breakdown(service):

    # preload cache
    service.cache.set("product", "Hot product", ttl=1)

    # cache expire
    time.sleep(2)

    def user_request():
        service.get_product("product")

    threads = []

    for _ in range(10):
        t = threading.Thread(target=user_request)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


# Main Execution
if __name__ == "__main__":

    print("\nCACHE BREAKDOWN\n")
    service = ProductService()
    simulate_breakdown(service)

    print("\nCACHE BREAKDOWN With Mutex Lock\n")
    safe_service = SafeProductService()
    simulate_breakdown(safe_service)

    print("\nSimulation completed.")