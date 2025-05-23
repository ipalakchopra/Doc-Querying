# DOCUMENTATION QUERYING APPLICATION

#Importing Libraries
import streamlit as st
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

#Streamlit Variables
if "vector" not in st.session_state:
    st.session_state.vectors = Chroma(persist_directory="./db/chromadb_rsyslog",embedding_function=HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2'))

st.title("Doc-Querying")

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

document_chain = create_stuff_documents_chain(llm, prompt)
retriever = st.session_state.vectors.as_retriever()

retrieval_chain = create_retrieval_chain(retriever, document_chain)

prompt = st.text_input("Input your prompt here")

if prompt:
    start = time.process_time()
    response = retrieval_chain.invoke({"input":prompt})
    print("Response time: ", time.process_time()-start)
    st.write(response['answer'])

    with st.expander("Doc Similarity Search"):
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("---------------------------------")
print("Response time:", time.process_time()-start)

#print(llm.invoke("What is kafka"))
