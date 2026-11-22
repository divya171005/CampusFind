import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from pymongo import MongoClient
from bson import ObjectId

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="Campus Lost & Found Portal", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

collection = None
if os.getenv("MONGODB_URI"):
    try:
        mongo = MongoClient(os.getenv("MONGODB_URI"), serverSelectionTimeoutMS=2500)
        mongo.admin.command("ping")
        collection = mongo[os.getenv("MONGODB_DATABASE", "campus_lost_found")]["items"]
    except Exception:
        collection = None

items_memory = []

class ItemCreate(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    category: str = Field(min_length=2, max_length=50)
    item_type: str = Field(pattern="^(Lost|Found)$")
    description: str = Field(min_length=5, max_length=1500)
    location: str = Field(min_length=2, max_length=120)
    date_seen: str = Field(min_length=4, max_length=30)
    contact_name: str = Field(min_length=2, max_length=80)
    contact_email: str = Field(min_length=5, max_length=120)

def serialize(doc):
    return {
        "id": str(doc.get("_id", doc.get("id", ""))),
        "title": doc["title"],
        "category": doc["category"],
        "item_type": doc["item_type"],
        "description": doc["description"],
        "location": doc["location"],
        "date_seen": doc["date_seen"],
        "contact_name": doc["contact_name"],
        "contact_email": doc["contact_email"],
        "status": doc.get("status", "Open"),
        "created_at": doc.get("created_at", "")
    }

@app.get("/")
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")

@app.get("/api/health")
def health():
    return {"status": "ok", "database": "connected" if collection is not None else "in-memory demo mode"}

@app.get("/api/items")
def get_items(
    q: Optional[str] = Query(default=None, max_length=100),
    item_type: Optional[str] = Query(default=None, pattern="^(Lost|Found)$"),
    category: Optional[str] = Query(default=None, max_length=50),
    status: Optional[str] = Query(default="Open", pattern="^(Open|Resolved|All)$")
):
    if collection is not None:
        query = {}
        if q:
            query["$or"] = [
                {"title": {"$regex": q, "$options": "i"}},
                {"description": {"$regex": q, "$options": "i"}},
                {"location": {"$regex": q, "$options": "i"}}
            ]
        if item_type:
            query["item_type"] = item_type
        if category:
            query["category"] = category
        if status != "All":
            query["status"] = status
        docs = list(collection.find(query).sort("_id", -1).limit(100))
        return {"items": [serialize(d) for d in docs]}

    docs = list(reversed(items_memory))
    if q:
        term = q.lower()
        docs = [d for d in docs if term in (d["title"] + " " + d["description"] + " " + d["location"]).lower()]
    if item_type:
        docs = [d for d in docs if d["item_type"] == item_type]
    if category:
        docs = [d for d in docs if d["category"] == category]
    if status != "All":
        docs = [d for d in docs if d["status"] == status]
    return {"items": [serialize(d) for d in docs[:100]]}

@app.post("/api/items", status_code=201)
def create_item(item: ItemCreate):
    doc = item.model_dump()
    doc.update({"status": "Open", "created_at": datetime.now(timezone.utc).isoformat()})
    if collection is not None:
        result = collection.insert_one(doc)
        doc["_id"] = result.inserted_id
    else:
        doc["id"] = str(len(items_memory) + 1)
        items_memory.append(doc)
    return {"item": serialize(doc)}

@app.patch("/api/items/{item_id}/resolve")
def resolve_item(item_id: str):
    if collection is not None:
        try:
            result = collection.update_one({"_id": ObjectId(item_id)}, {"$set": {"status": "Resolved"}})
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid item ID")
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        doc = collection.find_one({"_id": ObjectId(item_id)})
        return {"item": serialize(doc)}
    for doc in items_memory:
        if str(doc.get("id")) == item_id:
            doc["status"] = "Resolved"
            return {"item": serialize(doc)}
    raise HTTPException(status_code=404, detail="Item not found")
