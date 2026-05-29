"""
02 - ROUTING & VALIDATION: Pydantic Models & Request Bodies

Learn:
- Creating Pydantic schemas for request validation
- Using response models
- Path parameters vs query parameters vs request body
- Status codes and proper HTTP semantics
- Dependency injection basics

Run: uvicorn main:app --reload
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

# ================================
# PYDANTIC SCHEMAS (Data Validation)
# ================================

class ItemCreate(BaseModel):
    """Schema for creating an item"""
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=500, description="Item description")
    price: float = Field(..., gt=0, description="Item price (must be positive)")
    stock: int = Field(default=0, ge=0, description="Stock quantity")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "MacBook Pro",
                "description": "High-performance laptop",
                "price": 1999.99,
                "stock": 5
            }
        }


class ItemUpdate(BaseModel):
    """Schema for updating an item (all fields optional)"""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)


class ItemResponse(BaseModel):
    """Schema for API responses"""
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "MacBook Pro",
                "description": "High-performance laptop",
                "price": 1999.99,
                "stock": 5
            }
        }


# ================================
# FASTAPI APP & DATABASE
# ================================

app = FastAPI(
    title="02 - Routing & Validation",
    description="Learn Pydantic validation and proper routing patterns",
    version="2.0.0"
)

# Simulated database
items_db = [
    {"id": 1, "name": "Item One", "description": "First item", "price": 9.99, "stock": 10},
    {"id": 2, "name": "Item Two", "description": "Second item", "price": 19.99, "stock": 5},
]


# ================================
# CRUD ENDPOINTS WITH VALIDATION
# ================================

@app.get("/items", response_model=list[ItemResponse])
def list_items(skip: int = 0, limit: int = 10):
    """Get all items with pagination"""
    return items_db[skip : skip + limit]


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    """Get a specific item by ID"""
    for item in items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item {item_id} not found"
    )


@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    """Create a new item with validation
    
    Pydantic automatically validates:
    - name: must be 1-100 chars
    - price: must be > 0
    - stock: must be >= 0
    """
    new_id = max([item["id"] for item in items_db]) + 1
    new_item = {
        "id": new_id,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "stock": item.stock
    }
    items_db.append(new_item)
    return new_item


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item_update: ItemUpdate):
    """Update an item (partial updates allowed)"""
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            update_data = item_update.dict(exclude_unset=True)
            items_db[i] = {**item, **update_data}
            return items_db[i]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item {item_id} not found"
    )


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    """Delete an item"""
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            items_db.pop(i)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item {item_id} not found"
    )


# ================================
# KEY CONCEPTS DEMONSTRATED
# ================================
# 1. Pydantic BaseModel - automatic validation & serialization
# 2. Field() - add constraints (min_length, gt, ge, etc.)
# 3. response_model - ensure response matches schema
# 4. status codes - use proper HTTP semantics
# 5. HTTPException - standardized error responses
