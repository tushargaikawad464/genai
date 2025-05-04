import sys, os
from rich import print

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from knowledge.data_loader.docs_loader import DocsLoader
from utils.utils import get_env_vars
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_aws import BedrockEmbeddings
from langchain_chroma import Chroma

env_vars = get_env_vars()

def get_text_splitter():
    return RecursiveCharacterTextSplitter(chunk_size=575, chunk_overlap=50)


def build_vector_store(doc_path, collection_name, embedder, splitter, persist_dir):
    loader = DocsLoader()
    docs = loader.pdf_loader(doc_path)
    chunks = splitter.split_documents(docs)
    
    vector_store = Chroma(
        embedding_function=embedder,
        collection_name=collection_name,
        persist_directory=persist_dir,
    )
    vector_store.add_documents(chunks)
    
    return vector_store


def main():
    org_pdf_path = "/home/supreme-controller/workitems/python/genai/knowledge/data_source/Organizational_Identity.pdf"
    tech_pdf_path = "/home/supreme-controller/workitems/python/genai/knowledge/data_source/Technical_Team_Roles.pdf"

    embedder = BedrockEmbeddings(model_id=env_vars["EMBEDDING_MODEL_ID"], region_name=env_vars["REGION"])
    splitter = get_text_splitter()

    org_vector_store = build_vector_store(org_pdf_path, "org_kb", embedder, splitter, "./chroma_org_db")
    tech_vector_store = build_vector_store(tech_pdf_path, "tech_kb", embedder, splitter, "./chroma_tech_db")

    manager_query = "What is the mission of the organization?"
    engineer_query = "What are the responsibilities of DevOps Engineers?"

    print("\n--- Manager (Org) Query ---")
    org_results = org_vector_store.similarity_search(manager_query)
    org_results_content = ""
    for res in org_results:
        org_results_content += res.page_content + "\n"

    print(org_results_content)


    print("\n--- Engineer (Tech) Query ---")
    tech_results = tech_vector_store.similarity_search(engineer_query)
    tech_results_content = ""
    for res in tech_results:
        tech_results_content += res.page_content + "\n"

    print(tech_results_content)
    
if __name__ == "__main__":
    main()
