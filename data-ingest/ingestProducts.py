# ingest_products.py

import pandas as pd
import os
from pinecone import Pinecone
from openai import AzureOpenAI
from tqdm import tqdm
from dotenv import load_dotenv
load_dotenv()

# Load environment variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX")

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")  # Model deployment in Azure portal

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    api_version="2023-05-15"
)

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
#pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
#index = pinecone.Index(PINECONE_INDEX_NAME)

# Load CSV
df = pd.read_csv("data-ingest/sample_catalog.csv")

def generate_embedding(text):
    try:
        response = client.embeddings.create(
            input=[text],
            model=AZURE_DEPLOYMENT_NAME  # Name of your embedding model deployment
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Embedding generation failed for text: {text[:100]}... Error: {e}")
        return None
# Prepare data for Pinecone
vectors_to_upsert = []

for _, row in tqdm(df.iterrows(), total=len(df)):
    #text_to_embed = f"{row['title']} {row['description']} Brand: {row['brand']} Category: {row['category']} Color: {row['color'] Gender: {row['gender']}"
    text_to_embed = f"{row['title']}. {row['description']}. Brand: {row['brand']}. Category: {row['category']}. Color: {row['color']}. Gender: {row['gender']}"
    embedding = generate_embedding(text_to_embed)
    if embedding is None:
        continue
    metadata = {
        "product_id": row["id"],
        "page_content": f"{row['title']}. {row['description']}. Brand: {row['brand']}. Category: {row['category']}. Color: {row['color']}. Gender: {row['gender']}",
        "title": row["title"],
        "description": row["description"],
        "brand": row["brand"],
        "category": row["category"],
        "price": row["price"],
        "color": row["color"],
        "size": row["size"],
        "material": row["material"],
        "gender": row["gender"]
    }

    #vectors_to_upsert.append((row["id"], embedding, metadata))
    vectors_to_upsert.append((str(row["id"]), embedding, metadata))


# Batch upsert to Pinecone
batch_size = 50
for i in range(0, len(vectors_to_upsert), batch_size):
    batch = vectors_to_upsert[i:i+batch_size]
    #print(f"Product to be inserted!: {batch}")
    index.upsert(vectors=batch)

print("✅ Product ingestion completed!")
