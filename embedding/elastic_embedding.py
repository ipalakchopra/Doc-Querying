from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain.text_splitter import RecursiveCharacterTextSplitter

import requests
from bs4 import BeautifulSoup

def get_sitemap_urls(sitemap_url, keyword=None):
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.content, "xml")
    urls = [loc.text for loc in soup.find_all("loc")]
    if keyword:
        urls = [url for url in urls if keyword in url]
    return urls

# Get filtered URLs
urls = get_sitemap_urls("https://www.elastic.co/sitemap.xml", keyword="guide")

# Manually exclude broken URLs if needed
urls = [url for url in urls if "disk-usage" not in url]

# Then load with LangChain
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader(urls)  # limit to a few to test
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
documents=text_splitter.split_documents(docs)
print(documents)

db = Chroma.from_documents(persist_directory="./chromadb_elastic", documents=documents,embedding=HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2'))



print(f"Loaded {len(docs)} docs.")
