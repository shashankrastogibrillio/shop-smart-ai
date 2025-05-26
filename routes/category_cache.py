# routes/category_cache.py

from fastapi import APIRouter
from backend.utils.categoryCache import refresh_category_cache
from pinecone import Pinecone
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

@router.post("/refresh-category-cache")
def refresh_category_cache_route():
    try:
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index = pc.Index(os.getenv("PINECONE_INDEX"))
        categories = refresh_category_cache(index)
        return {"message": f"Category cache refreshed with {len(categories)} categories."}
    except Exception as e:
        return {"error": str(e)}
