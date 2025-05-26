# backend/utils/categoryCache.py

import json
import os
from pathlib import Path
from tqdm import tqdm


CACHE_FILE = Path("backend/cache/categories.json")

def load_cached_categories():
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return []

def save_categories_to_cache(categories):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(categories, f, indent=2)

def refresh_category_cache(index):
    print("🔁 Refreshing category cache from Pinecone...")

    # Step 1: Get all vector IDs in the index
    stats = index.describe_index_stats()
    total_vectors = stats["total_vector_count"]
    print(f"📦 Total vectors in index: {total_vectors}")

    all_categories = set()
    namespace = ""

    # Step 2: Fetch metadata in batches
    # You’ll need to store vector IDs during upsert to fetch them here.
    # For now, we assume vector IDs are like product_1, product_2, ...

    all_ids = [f"product_{i}" for i in range(1, total_vectors + 1)]
    batch_size = 50
    for i in tqdm(range(0, len(all_ids), batch_size), desc="Fetching metadata"):
        batch_ids = all_ids[i:i + batch_size]
        response = index.fetch(ids=batch_ids, namespace=namespace)
        vectors = response.vectors
        for v in vectors.values():
            meta = v.metadata
            category = meta.get("category")
            if category:
                all_categories.add(category)

    categories = sorted(list(all_categories))
    save_categories_to_cache(categories)
    print(f"✅ Saved {len(categories)} unique categories to cache.")
    return list(categories)
