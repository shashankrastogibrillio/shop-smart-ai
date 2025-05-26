from pinecone import Pinecone, ServerlessSpec  # New Pinecone SDK
#from langchain_community.vectorstores import Pinecone as CommunityPinecone
from langchain_pinecone import PineconeVectorStore
#from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai import AzureOpenAIEmbeddings

import os
from backend.utils.filters import apply_filters
from langchain_community.vectorstores import Pinecone as CommunityPinecone

from dotenv import load_dotenv
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
#PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")


def load_retriever(query, filters):
    try:

       # Create Pinecone client (no init or environment)
        pc = Pinecone(api_key=PINECONE_API_KEY)
        #print("Available Pinecone indexes:", pc.list_indexes().names())
        
        # This line checks if the index exists and can access it
        index = pc.Index(PINECONE_INDEX_NAME)
        print("index.describe_index_stats()",index.describe_index_stats())
        #embedder = AzureOpenAIEmbeddings(openai_api_key=api_key)

        # Convert filters into Pinecone metadata filter format
        pinecone_filter = {}
        if filters:
            for key in [ "color", "size", "brand", "gender", "category"]:
                value = filters.get(key)
                if value:
                   # Normalize: lowercase and strip spaces
                   normalized_value = value.lower().strip()
                   pinecone_filter[key] = {"$eq": value}
                   # Case-insensitive "contains" match using regex
                   #pinecone_filter[key] = {"$regex": f"(?i).*{value}.*"}
       
        print("pinecone_filter:::", pinecone_filter)

        embedder = AzureOpenAIEmbeddings(
            openai_api_key=api_key,
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION")
        )

        #embedding = embedder.embed_query("Men Cotton T-Shirt")
        #print(f"Query embedding: {embedding[:5]}...")  # Just print a snippet
        #results = index.query(vector=embedding, top_k=5, include_metadata=True)
        #print("results:::", results)

        # Inject filter hints into the query for better semantic search
        filter_context = ", ".join([f"{v} {k}" for k, v in filters.items()])
        modified_query = f"Looking for {filter_context}. Query: {query}"

        #filter_prefix = ". ".join([f"{k}: {v}" for k, v in filters.items()])
        #modified_query = f"{filter_prefix}. {query}"
        embedding = embedder.embed_query(modified_query)

        # Raw vector search to debug
        raw_results = index.query(vector=embedding, top_k=15, include_metadata=True, filter=pinecone_filter)
        print("******RAW Results from Pinecone:*****", raw_results)

        vectorstore = PineconeVectorStore(
            index_name=PINECONE_INDEX_NAME, 
            embedding=embedder, 
            text_key="page_content"
        )
        #vectorstore = LangchainPinecone(index, embedder.embed_query, "text")


        #retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        retriever = vectorstore.as_retriever(
            search_type="mmr",  # Max marginal relevance for diversity
            search_kwargs={"k": 5,
                "filter": pinecone_filter if pinecone_filter else None,
                "lambda_mult": 0.6  # Balance semantic vs metadata relevance
            }
        )
        print("retriever.search_type:::", retriever.search_type)
        #retriever = apply_filters(retriever, filters)
        return retriever
    except Exception as e:
        raise Exception(f"Failed to connect to Pinecone or load retriever: {str(e)}")
