from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from backend.chains.shoppingChain import build_shopping_assistant
from backend.utils.filterExtractor import extract_filters_from_query
from routes.category_cache import router as category_cache_router
import uvicorn
import json

app = FastAPI()

app.include_router(category_cache_router, prefix="/admin", tags=["Admin"])


@app.post("/search")
async def search_products(request: Request):
    body = await request.json()
    session_id = body.get("session_id", "anonymous")
    query = body.get("query")
    filters = body.get("filters", {})
    if not query:
        raise HTTPException(status_code=400, detail="Missing 'query' in request body")

    try:
        #user_filters={}
        user_filters = extract_filters_from_query(query)
        chain = build_shopping_assistant(session_id, query, user_filters)
        #chain = build_shopping_assistant(session_id, filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing shopping assistant: {str(e)}")

    async def response_generator():
        try:
            #response = await chain.acall({"question": query}, callbacks=[])
            response = await chain.acall({"question": query, "chat_history": []}, callbacks=[])
            answer = response.get("answer", "")
            source_documents = response.get("source_documents", [])

            #print("Response from chain:", response)
            #print("Answer:", answer)
            print("Source Documents:", source_documents)
            
            if not source_documents:
                yield json.dumps({"message": "No Products Found"})
            else:
                for doc in source_documents:
                    print("doc.page_content:::", doc.page_content)
                    product_data = {
                        "id": doc.metadata.get("ID", "No ID"),
                        "title": doc.metadata.get("title", "No title available"),
                        "description": doc.metadata.get("description", "No description available"),
                        "color": doc.metadata.get("color", "No color available"),
                    }
                    yield json.dumps(product_data)
        except Exception as e:
            yield f"Error generating response: {str(e)}"

    return StreamingResponse(response_generator(), media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
