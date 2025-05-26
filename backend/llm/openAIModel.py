#from langchain.chat_models import AzureChatOpenAI
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

def load_llm():
    try:

        api_key = os.getenv("AZURE_OPENAI_CHAT_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_CHAT_ENDPOINT")
        deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
        version = os.getenv("AZURE_OPENAI_CHAT_API_VERSION")

        print("AZURE_OPENAI_API_VERSION:", version)  # Add this
        print("Calling AzureChatOpenAI with:", {
            "api_key": api_key,
            "azure_endpoint": endpoint,
            "deployment_name": deployment,
            "api_version": version
        })

        return AzureChatOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            deployment_name=deployment,
            api_version=version,
            temperature=0.3,
            streaming=True
        )
    except Exception as e:
        raise Exception(f"Failed to load Open AI: {str(e)}")
    

