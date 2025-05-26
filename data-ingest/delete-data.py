from pinecone import Pinecone
import os
from dotenv import load_dotenv
load_dotenv()

# Load environment variable or use directly
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX")

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

# 🔥 Delete all vectors in the index
index.delete(delete_all=True)

print("✅ All vectors deleted from the index.")
