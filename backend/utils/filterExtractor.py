from openai import AzureOpenAI
import os
import json
from dotenv import load_dotenv
load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_CHAT_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_CHAT_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_CHAT_API_VERSION")
)

def extract_filters_from_query(query: str) -> dict:
    prompt = f"""
Extract shopping filters from the following query. Return only fields that are mentioned.

Query: "{query}"

Output JSON format:
{{
  "category": "...",
  "color": "...",
  "size": "...",
  "brand": "...",
  "gender": "...",
  "min_price": ...,
  "max_price": ...
}}

Leave out keys that are not relevant.
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    try:
        filter=json.loads(response.choices[0].message.content.strip())
        print("In extract_filters_from_query *****   filter:", filter)
        return filter
    except Exception as e:
        print("❌ Failed to parse filters:", e)
        return {}
