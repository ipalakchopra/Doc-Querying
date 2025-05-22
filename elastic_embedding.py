from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders.sitemap import SitemapLoader

#loader = WebBaseLoader("https://www.rsyslog.com/doc/")
sitemap_loader = SitemapLoader(web_path="https://www.elastic.co/docs/sitemap.xml")
docs = sitemap_loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
documents=text_splitter.split_documents(docs)
print(documents)

db = Chroma.from_documents(persist_directory="./chromadb_elastic", documents=documents,embedding=HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2'))

print(db.search("MySQL","similarity")[0].page_content)