class CacheDB:
    def __init__(self):
        self.cache = {}

    def is_updated(self, product_name, product_price):
        if product_name in self.cache and self.cache[product_name] == product_price:
            return True
        return False

    def update_cache(self, product_name, product_price):
        self.cache[product_name] = product_price
