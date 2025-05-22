# Vector Embedding from Doc

#Libraries
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

#Load Docs
loader = PyPDFLoader("Data/kafka.pdf")
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
documents=text_splitter.split_documents(docs)
print(documents)

#Vector Embeddings
db = Chroma.from_documents(persist_directory="./chromadb", documents=documents,embedding=HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2'))

vectordb = Chroma(persist_directory="./chromadb",embedding_function=HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2'))
print(db.search("kafka","similarity")[0].page_content)
print()
print(vectordb.search("kafka","similarity")[0].page_content)
