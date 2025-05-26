Setup
1. Install python version 3.11.12
2. Clone shop-smart-ai repo
3. Checkout main branch 
4. Update .env file with following properties -
    a. Open AI key for embedding -
        AZURE_OPENAI_ENDPOINT=
        AZURE_OPENAI_DEPLOYMENT_NAME=text-embedding-3-small
        AZURE_OPENAI_API_VERSION=2024-12-01-preview
        OPENAI_API_TYPE=azure
    b. Open AI key for Chat -
        AZURE_OPENAI_CHAT_API_KEY=
        AZURE_OPENAI_CHAT_ENDPOINT=https://shash-ma3h6roa-japaneast.cognitiveservices.azure.com/
        AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4.1
        AZURE_OPENAI_CHAT_API_VERSION=2024-12-01-preview
5. Simialrly add follwoing properties for pinecone index -
    PINECONE_API_KEY=
    PINECONE_ENVIRONMENT=us-east-1
    PINECONE_INDEX=shop-smart-index
6. Run requirements.txt to install all required libraries
7. Update data-ingest/sample_Catalog.csv to change the products data.
8. Use following command to set up products in pinecone index
    python data-ingest/ingestProducts.py
9. Run following command to  refresh the category cache (currenly stored in a file @ /backend/cache/categories.json)
    python routes/category_cache.py     
10. Use  python app.py   to run the app