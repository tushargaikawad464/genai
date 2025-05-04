from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, TextLoader
import os


class DocsLoader:
    def __init__(self):
        pass

    def web_loader(self, url):
        loader = WebBaseLoader(url)
        data = loader.load()
        return data
    
    def text_loader(self, file_path):
        loader = TextLoader(file_path, encoding="utf-8")
        data = loader.load()
        return data
    
    def pdf_loader(self, file_path):
        loader = PyPDFLoader(file_path)
        data = loader.load()
        return data
        

