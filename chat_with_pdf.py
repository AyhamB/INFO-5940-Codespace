# chat_with_pdf.py
import os
import io
import streamlit as st
from typing import List

import pandas as pd  

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FakeEmbeddings  
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_openai import ChatOpenAI

# App Setup
st.set_page_config(page_title="💬 LangChain RAG Chat", layout="wide")
st.title("💬 RAG System with LangChain + Chroma")

#  Initialize OpenAI 
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    st.error("⚠️ API_KEY not set. Run this in your terminal first:\n\nexport API_KEY='your_actual_API_key_here'")
    st.stop()

# embedding
embeddings = FakeEmbeddings(size=1536)

#  Use GPT-4o for conversation
llm = ChatOpenAI(
    model="openai.gpt-4o",
    openai_api_key=API_KEY,
    openai_api_base="https://api.ai.it.cornell.edu/v1",
    temperature=0.2
)

# File Upload UI
st.sidebar.header("📥 Upload Documents (.txt, .pdf, .xlsx)")
uploaded_files = st.sidebar.file_uploader(
    "Choose files",
    type=["txt", "pdf", "xlsx"],
    accept_multiple_files=True
)

# Persistent session state
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Upload a .txt, .pdf, or .xlsx file and ask me a question!"}
    ]


# File Processing Function
def load_and_split(file) -> List:
    """Reads and splits a text, PDF, or Excel file into LangChain Documents."""
    temp_path = f"./temp_{file.name}"

    if file.name.endswith(".txt"):
        # Plain text
        text = file.read().decode("utf-8", errors="ignore")
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(text)
        loader = TextLoader(temp_path)

    elif file.name.endswith(".pdf"):
        # PDF
        with open(temp_path, "wb") as f:
            f.write(file.read())
        loader = PyPDFLoader(temp_path)

    elif file.name.endswith(".xlsx"):
        df = pd.read_excel(file)
        text = df.to_string(index=False) 
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(text)
        loader = TextLoader(temp_path)

    else:
        raise ValueError("Unsupported file format!")

    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    return chunks

# Build Vectorstore (Chroma)
if uploaded_files:
    all_chunks = []
    for file in uploaded_files:
        try:
            chunks = load_and_split(file)
            all_chunks.extend(chunks)
            st.sidebar.success(f"✅ Processed: {file.name} ({len(chunks)} chunks)")
        except Exception as e:
            st.sidebar.error(f"❌ Failed to read {file.name}: {e}")

    if all_chunks:
        st.session_state.vectorstore = Chroma.from_documents(all_chunks, embeddings)
        
# Chat Interface
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input(
    "Ask a question about your documents…",
    disabled=(st.session_state.vectorstore is None)
)

if user_input and st.session_state.vectorstore:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    #  LangChain RetrievalQA chain
    retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 5})
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

    with st.chat_message("assistant"):
        result = qa_chain.invoke({"query": user_input})
        answer = result["result"]
        st.write(answer)

        # Display source text snippets
        with st.expander("🔎 Sources used"):
            for i, doc in enumerate(result["source_documents"], start=1):
                st.markdown(f"**[{i}] Source: {doc.metadata.get('source', 'Unknown')}**")
                st.write(doc.page_content[:400] + "...")
                st.markdown("---")

    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": answer})
