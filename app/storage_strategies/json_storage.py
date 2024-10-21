import json
import os
from app.storage_strategy import StorageStrategy

class JsonStorageStrategy(StorageStrategy):
    def save(self, data):
        if not os.path.exists('data'):
            os.makedirs('data')
        with open('data/products.json', 'w') as file:
            json.dump(data, file, indent=4)
