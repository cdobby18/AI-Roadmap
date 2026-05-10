from fastapi import FastAPI

# FastAPI app instance
app = FastAPI()

# Sample data storage
items = [
    {"id": 1, "name": "Item One"},
    {"id": 2, "name": "Item Two"},
    {"id": 3, "name": "Item Three"},
]

# Root route
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Get all items
@app.get("/items")
def get_items():
    return items

# Get item by ID
@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}

# Create new item
@app.post("/items")
def create_item(item: dict):
    items.append(item)
    return item