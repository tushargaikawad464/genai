import os
import sys
from langchain_aws import BedrockEmbeddings
from langchain_community.retrievers import WikipediaRetriever
from langchain_chroma import Chroma
from langchain_aws import BedrockLLM, ChatBedrockConverse
from chromadb import PersistentClient
from langchain.retrievers.multi_query import MultiQueryRetriever

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.utils import get_env_vars

env_vars = get_env_vars()

def wiki_retriever(query, top_k=2, lang="en"):
    retriever = WikipediaRetriever(top_k_results=top_k, lang=lang)
    docs = retriever.invoke(query)
    return docs

def get_vector_store(collection_name, persist_directory):
    client = PersistentClient(path=persist_directory)
    existing_collections = [col.name for col in client.list_collections()]
    
    if collection_name in existing_collections:
        vector_store = Chroma(
            collection_name=collection_name,
            persist_directory=persist_directory,
            embedding_function=BedrockEmbeddings(
                model_id=env_vars["EMBEDDING_MODEL_ID"],
                region_name=env_vars["REGION"]
            )
        )
        print(f"Loaded Existing Collection: {collection_name}")
        return vector_store
    else:
        print(f"Existing Collection Not Found: {collection_name}")
        return None


def vanilla_retriver(query, collection_name, persist_directory):
    
    vector_store = get_vector_store(collection_name, persist_directory)
    
    if vector_store:
        info_retriever = vector_store.as_retriever(
            search_kwargs={"k": 1}, # vanilla_retriver
            )
        result = info_retriever.invoke(query)
        return result
    else:
        return f"Existing Collection Not Found: {collection_name}"
    
def mmr_retriver(query, collection_name, persist_directory):
    
    vector_store = get_vector_store(collection_name, persist_directory)
    
    if vector_store:
        info_retriever = vector_store.as_retriever(
            search_kwargs={"k": 2, "lambda_mult": 0.5}, # Maximal Marginal Relevance based_retriver, lambda_mult value between 0-1, 1 is similar to vanilla 0 is relevance -diversity
            search_type = "mmr"
            )
        result = info_retriever.invoke(query)
        return result
    else:
        return f"Existing Collection Not Found: {collection_name}"
    
def multi_query_retriver(query, collection_name, persist_directory):
    
    vector_store = get_vector_store(collection_name, persist_directory)
    
    if vector_store:
        info_retriever = MultiQueryRetriever.from_llm(
            retriever=vector_store.as_retriever(
                search_kwargs={"k": 3}
            ),
            
            llm=ChatBedrockConverse(
                model=env_vars["MODEL_ID"],
                region_name=env_vars["REGION"]
            ),
        )
        result = info_retriever.invoke(query)
        return result
    else:
        return f"Existing Collection Not Found: {collection_name}"

if __name__ == "__main__":
    query = "explain role and responsiblity"
    persist_directory = "/home/supreme-controller/workitems/python/genai/chroma_tech_db"
    collection_name = "tech_kb"

    # result = vanilla_retriver(query, collection_name, persist_directory) 
    # result = mmr_retriver(query, collection_name, persist_directory) 
    result = multi_query_retriver(query, collection_name, persist_directory)
    print(len(result))
    for i, doc in enumerate(result):
        print(f"\n----------result {i}-------")
        print(doc.page_content)

    # Optionally, retrieve from Wikipedia
    # wiki_docs = wiki_retriever(query)
    # print(wiki_docs)