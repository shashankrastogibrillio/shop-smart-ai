**Setup**
1.	Install python version 3.11.12
2.	Clone shop-smart-ai repo
3.	Checkout main branch 
4.	Update .env file with following properties -
a.	Open AI key for embedding -
    •	AZURE_OPENAI_ENDPOINT=
    •	AZURE_OPENAI_DEPLOYMENT_NAME=text-embedding-3-small
    •	AZURE_OPENAI_API_VERSION=2024-12-01-preview
    •	OPENAI_API_TYPE=azure
b.	Open AI key for Chat -
    •	AZURE_OPENAI_CHAT_API_KEY=
    •	AZURE_OPENAI_CHAT_ENDPOINT=
    •	AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4.1
    •	AZURE_OPENAI_CHAT_API_VERSION=2024-12-01-preview
6.	Similarly add following properties for pinecone index -
    •	PINECONE_API_KEY=
    •	PINECONE_ENVIRONMENT=us-east-1
    •	PINECONE_INDEX=
7.	Run requirements.txt to install all required libraries
8.	Update data-ingest/sample_Catalog.csv to change the products data.
9.	Use following command to set up products in pinecone index
       _ python data-ingest/ingestProducts.py_
10.	Run following command to  refresh the category cache (currenly stored in a file @ /backend/cache/categories.json)
       _ python routes/category_cache.py_
11.	Use _python app.py_ to run the app
