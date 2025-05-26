import os
from pinecone import Pinecone
from dotenv import load_dotenv
load_dotenv()

# Load environment variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX")

# Initialize Pinecone environment
#pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment="us-west1-gcp")

# Index name
index_name = "product-index"  # Make sure the index name matches what you set earlier



results = index.search(
    namespace="example-namespace", 
    query={
        "inputs": {"text": "Disease prevention"}, 
        "top_k": 2
    },
    fields=["category", "chunk_text"]
)

print(results)

# Query embedding (replace with actual product embedding)
query_embedding = [
    0.12, 0.23, -0.34, 0.5, 0.1, -0.22, 0.8, 0.3,  # Example dummy vector
]

# Connect to the Pinecone index
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

# Perform the query (find top 3 similar products)
response = index.query(
    queries=[query_embedding],
    top_k=3,  # Retrieve top 3 similar results
    include_metadata=True  # Include metadata like title, description
)

# Display results
print("Top 3 Similar Products:")
for match in response['results'][0]['matches']:
    print(f"Product ID: {match['id']}, Score: {match['score']}")
    print(f"Product Title: {match['metadata']['title']}")
    print(f"Description: {match['metadata']['description']}")
    print("--------")
