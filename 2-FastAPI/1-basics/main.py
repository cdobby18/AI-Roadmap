"""
01 - BASICS: Hello FastAPI

Learn:
- Creating a FastAPI application
- Defining basic GET/POST endpoints
- Understanding Uvicorn server
- Testing with Swagger UI (/docs)

Run: uvicorn main:app --reload
Visit: http://localhost:8000/docs
"""

from fastapi import FastAPI

# Create FastAPI application instance
app = FastAPI(
    title="01 - FastAPI Basics",
    description="Learn the fundamentals of FastAPI",
    version="1.0.0"
)

# Sample data storage
items = [
    {"id": 1, "name": "Item One", "price": 9.99},
    {"id": 2, "name": "Item Two", "price": 19.99},
    {"id": 3, "name": "Item Three", "price": 29.99},
]


# ================================
# BASIC ENDPOINTS
# ================================

@app.get("/")
def read_root():
    """Root endpoint - returns a greeting"""
    return {"message": "Welcome to FastAPI!", "version": "1.0.0"}


@app.get("/items")
def get_items():
    """Get all items"""
    return {"items": items, "total": len(items)}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    """Get a specific item by ID"""
    for item in items:
        if item["id"] == item_id:
            return {"item": item}
    return {"error": "Item not found"}, 404


@app.post("/items")
def create_item(name: str, price: float):
    """Create a new item
    
    Query parameters:
    - name: Item name (str)
    - price: Item price (float)
    """
    new_item = {
        "id": max([item["id"] for item in items]) + 1,
        "name": name,
        "price": price
    }
    items.append(new_item)
    return {"message": "Item created", "item": new_item}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """Delete an item by ID"""
    for i, item in enumerate(items):
        if item["id"] == item_id:
            deleted = items.pop(i)
            return {"message": "Item deleted", "item": deleted}
    return {"error": "Item not found"}, 404


# ================================
# UNDERSTAND: Path vs Query Parameters
# ================================

@app.get("/search")
def search_items(keyword: str = None, min_price: float = 0):
    """Search items by keyword and price
    
    This demonstrates QUERY PARAMETERS (after ?)
    Example: /search?keyword=Item&min_price=15
    """
    results = []
    for item in items:
        if keyword and keyword.lower() not in item["name"].lower():
            continue
        if item["price"] >= min_price:
            results.append(item)
    return {"results": results, "count": len(results)}
