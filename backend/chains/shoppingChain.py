from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from backend.llm.openAIModel import load_llm
from backend.memory.redisMemory import load_memory
from backend.retrievers.productRetriever import load_retriever


def build_shopping_assistant(session_id, query, user_filters):
    llm = load_llm()
   # memory = load_memory(session_id)
    retriever = load_retriever(query, user_filters)

    # Custom prompt
    qa_prompt = PromptTemplate.from_template("""
You are a helpful shopping assistant. Based on the following product data, answer the user's query.

If relevant products are found, list them with their title and description in bullet points. If no relevant products are found, respond with: "No Products Found".

Product Data:
{context}

User Query: {question}
""")
    
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
       # memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": qa_prompt}
    )
    return chain
