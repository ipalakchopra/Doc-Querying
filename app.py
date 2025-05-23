# DOCUMENTATION QUERYING APPLICATION

#Importing Libraries
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import time
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

#Load Environment Variables
load_dotenv()

#Langsmith Tracing
os.environ["LANGCHAIN_HANDLER"] = "langsmith"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGSMITH_PROJECT"] = "Doc-Querying"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
#client = Client()
start = time.process_time()

# Mistral LLM
llm = OllamaLLM(model="mistral:7b")

#Prompt Template
prompt = ChatPromptTemplate.from_template("""
Answer the following question based only on the provided context.
Think step by step before providing a detailed answer.
<context>
{context}
</context>
Question: {input}""")

#Vector DB
vectordb = Chroma(persist_directory="./chromadb_elastic",embedding_function=HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2'))

#Retriever
retriever = vectordb.as_retriever()

#Chains
document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever,document_chain)
print(retrieval_chain.invoke({'input':"Information on the doc"})['answer'])
print("Response time:", time.process_time()-start)
print(retrieval_chain.invoke({'input':"How to setup and elasticsearch cluster"})['answer'])

#print(llm.invoke("What is kafka"))
