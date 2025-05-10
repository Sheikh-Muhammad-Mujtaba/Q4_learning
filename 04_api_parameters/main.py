from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float

app = FastAPI(
    title="FastAPI Parameters",
    description="This is a simple API to demonstrate FastAPI parameters",
    version="1.0.0",
)

@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(
        ...,  # ... means the parameter is required
        title="The ID of the item",
        description="A unique identifier for the item",
        ge=1  # ge = greater than or equal to 1
    )
):
    
    return {"item_id": item_id}


@app.get("/items/")
async def read_items(
    
    q: str | None = Query(
        None,  # default value
        max_length=50,
        min_length=3,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
    ),
    
    skip: int = Query(0, ge=0),
    
    limit: int = Query(10, le=100)
):
    
    return {"q": q, "skip": skip, "limit": limit}
   
   
   
@app.put("/items/validated/{item_id}")
async def update_items(
    
    item_id: int = Path(
        ...,
        title="The ID of the item",
        ge=1
    ),
    
    q: str | None = Query(
        None,
        min_length=3,
    ),
    
    item: Item | None = Body(
        None,
        description="The item to update",
    )
    
):
    
    result = {"item_id": item_id}
    
    if q:
        result.update({"q": q})
    if item:
        result.update({"item": item.model_dump()})
    
    return result        