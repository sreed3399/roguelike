import yaml
import os

def create_items_from_yaml(file_path):
    with open(file_path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            items = []
            for item_data in data:
                # Assuming each item in YAML is a dictionary
                item = Item(**item_data)  # Assuming you have a class named Item
                items.append(item)
            return items
        except yaml.YAMLError as e:
            print("Error reading YAML:", e)


# Example usage:
class Item:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

# Assuming your YAML file looks like this:
# - name: Item1
#   price: 10
#   quantity: 5
# - name: Item2
#   price: 20
#   quantity: 3



dir_path = os.getcwd()  + "/resources/items.yaml"



print(dir_path)
items = create_items_from_yaml(dir_path)
for item in items:
    print("Name:", item.name)
    print("Price:", item.price)
    print("Quantity:", item.quantity)
    print()