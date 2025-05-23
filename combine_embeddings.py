from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

chroma1 = Chroma(persist_directory="./db/chromadb_kafka", embedding_function=embedding)
chroma2 = Chroma(persist_directory="./db/chromadb_rsyslog", embedding_function=embedding)
chroma3 = Chroma(persist_directory="./chromadb_elastic", embedding_function=embedding)

data1 = chroma1.get()
data2 = chroma2.get()
data3 = chroma3.get()

all_texts = data1['documents'] + data2['documents'] + data3['documents']
all_metas = data1['metadatas'] + data2['metadatas'] + data3['metadatas']

combined_chroma = Chroma.from_texts(
    texts=all_texts,
    embedding=embedding,
    metadatas=all_metas,
    persist_directory="./combined_chromadb"  
)

print(f"Combined DB created with {len(all_texts)} documents.")
