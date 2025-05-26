**Setup**
1.	Install python version 3.11.12
2.	Clone shop-smart-ai repo
3.	Checkout main branch 
4.	Update .env file with following properties - <br>
a.	Open AI key for embedding -  <br>
    •	AZURE_OPENAI_ENDPOINT= <br>
    •	AZURE_OPENAI_DEPLOYMENT_NAME=text-embedding-3-small  <br>
    •	AZURE_OPENAI_API_VERSION=2024-12-01-preview <br>
    •	OPENAI_API_TYPE=azure <br>
b.	Open AI key for Chat - <br>
    •	AZURE_OPENAI_CHAT_API_KEY= <br>
    •	AZURE_OPENAI_CHAT_ENDPOINT= <br>
    •	AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4.1 <br>
    •	AZURE_OPENAI_CHAT_API_VERSION=2024-12-01-preview <br>
6.	Similarly add following properties for pinecone index - <br>
    •	PINECONE_API_KEY= <br>
    •	PINECONE_ENVIRONMENT=us-east-1 <br>
    •	PINECONE_INDEX= <br>
7.	Run requirements.txt to install all required libraries
8.	Update data-ingest/sample_Catalog.csv to change the products data.
9.	Use following command to set up products in pinecone index  <br>
       _ python data-ingest/ingestProducts.py_
10.	Run following command to  refresh the category cache (currenly stored in a file @ /backend/cache/categories.json)  <br>
       _ python routes/category_cache.py_
11.	Use _python app.py_ to run the app
