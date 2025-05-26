import pinecone
import os
from dotenv import load_dotenv
load_dotenv()

def init_pinecone():
    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"),
        environment=os.getenv("PINECONE_ENVIRONMENT")
    )
