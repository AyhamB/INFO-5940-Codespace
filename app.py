import streamlit as st
import os
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.embeddings import Embeddings
from litellm import completion
import shutil
from typing import List
import requests
import json

# Load environment variables
load_dotenv()

# Set environment variables for litellm
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
if os.getenv("OPENAI_BASE_URL"):
    os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_BASE_URL")

# Page configuration
st.set_page_config(
    page_title="RAG Document Chat Application",
    page_icon="📚",
    layout="wide"
)

# Custom Embeddings class using litellm
class LiteLLMEmbeddings(Embeddings):
    """Custom embeddings using litellm for compatibility with various APIs"""

    def __init__(self, model: str = "text-embedding-ada-002"):
        self.model = model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents using direct API call"""
        # Direct API call using requests
        url = f"{os.getenv('OPENAI_BASE_URL')}/embeddings"
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "input": texts
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            raise ValueError(f"API error: {response.status_code} - {response.text}")

        # Parse JSON response
        response_json = response.json()

        # Extract embeddings
        if isinstance(response_json, dict) and 'data' in response_json:
            return [item['embedding'] for item in response_json['data']]
        else:
            raise ValueError("Invalid response format from embedding API")

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query"""
        # Reuse embed_documents for single query
        embeddings = self.embed_documents([text])
        return embeddings[0]

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "processed_files" not in st.session_state:
    st.session_state.processed_files = []

def extract_text_from_txt(file):
    """Extract text from a .txt file"""
    return file.read().decode("utf-8")

def extract_text_from_pdf(file):
    """Extract text from a .pdf file"""
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def process_documents(uploaded_files):
    """Process uploaded documents and extract text"""
    all_text = ""
    new_files = []

    for uploaded_file in uploaded_files:
        # Check if file was already processed
        if uploaded_file.name in st.session_state.processed_files:
            continue

        file_extension = uploaded_file.name.split(".")[-1].lower()

        try:
            if file_extension == "txt":
                text = extract_text_from_txt(uploaded_file)
            elif file_extension == "pdf":
                text = extract_text_from_pdf(uploaded_file)
            else:
                st.warning(f"Unsupported file format: {uploaded_file.name}")
                continue

            all_text += f"\n\n--- Content from {uploaded_file.name} ---\n\n{text}"
            new_files.append(uploaded_file.name)

        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
            continue

    return all_text, new_files

def create_vectorstore(text, existing_vectorstore=None):
    """Create or update vector store from text"""
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    # Create embeddings using litellm
    embeddings = LiteLLMEmbeddings(model="text-embedding-ada-002")

    # Create or update vector store
    if existing_vectorstore is None:
        vectorstore = Chroma.from_texts(
            texts=chunks,
            embedding=embeddings,
            persist_directory="./chroma_db"
        )
    else:
        # Add new chunks to existing vectorstore
        existing_vectorstore.add_texts(texts=chunks)
        vectorstore = existing_vectorstore

    return vectorstore

def get_rag_response(vectorstore, question, chat_history):
    """Get response using RAG with chat history"""
    # Create retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Retrieve relevant documents
    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])

    # Build messages for litellm
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that answers questions based on the provided context. "
                      "Use the context and chat history to provide accurate and relevant answers. "
                      "If you cannot find the answer in the context, say so."
        }
    ]

    # Add chat history
    for msg in chat_history:
        if isinstance(msg, HumanMessage):
            messages.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            messages.append({"role": "assistant", "content": msg.content})

    # Add current question with context
    messages.append({
        "role": "user",
        "content": f"Context:\n{context}\n\nQuestion: {question}"
    })

    # Get response from LLM using litellm
    try:
        response = completion(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            api_base=os.getenv("OPENAI_BASE_URL"),
            api_key=os.getenv("OPENAI_API_KEY")
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"LLM error: {str(e)}")
        raise

def handle_user_input(user_question):
    """Handle user question and generate response"""
    if st.session_state.vectorstore is None:
        st.warning("Please upload documents first!")
        return

    with st.spinner("Thinking..."):
        # Convert chat history to LangChain message format
        langchain_history = []
        for chat in st.session_state.chat_history:
            langchain_history.append(HumanMessage(content=chat["question"]))
            langchain_history.append(AIMessage(content=chat["answer"]))

        # Get response
        answer = get_rag_response(
            st.session_state.vectorstore,
            user_question,
            langchain_history
        )

    # Update chat history
    st.session_state.chat_history.append({
        "question": user_question,
        "answer": answer
    })

def main():
    st.title("📚 RAG Document Chat Application")
    st.markdown("Upload documents and chat with their content using AI-powered retrieval!")

    # Sidebar for document upload
    with st.sidebar:
        st.header("📁 Document Upload")
        uploaded_files = st.file_uploader(
            "Upload your documents (.txt or .pdf)",
            type=["txt", "pdf"],
            accept_multiple_files=True,
            help="You can upload multiple files at once"
        )

        if uploaded_files:
            if st.button("Process Documents", type="primary"):
                with st.spinner("Processing documents..."):
                    # Extract text from new files
                    text, new_files = process_documents(uploaded_files)

                    if text:
                        # Create or update vectorstore
                        st.session_state.vectorstore = create_vectorstore(
                            text,
                            st.session_state.vectorstore
                        )

                        # Update processed files list
                        st.session_state.processed_files.extend(new_files)

                        st.success(f"Successfully processed {len(new_files)} new document(s)!")
                    else:
                        st.info("No new documents to process.")

        # Display processed files
        if st.session_state.processed_files:
            st.markdown("---")
            st.subheader("📄 Processed Documents")
            for idx, filename in enumerate(st.session_state.processed_files, 1):
                st.text(f"{idx}. {filename}")

            if st.button("Clear All Documents"):
                st.session_state.chat_history = []
                st.session_state.vectorstore = None
                st.session_state.processed_files = []

                # Clean up chroma db directory
                if os.path.exists("./chroma_db"):
                    shutil.rmtree("./chroma_db")

                st.rerun()

    # Main chat interface
    st.markdown("---")

    # Chat input
    user_question = st.chat_input("Ask a question about your documents...")

    if user_question:
        handle_user_input(user_question)

    # Display chat history
    if st.session_state.chat_history:
        for i, chat in enumerate(st.session_state.chat_history):
            with st.chat_message("user"):
                st.write(chat["question"])

            with st.chat_message("assistant"):
                st.write(chat["answer"])
    else:
        # Welcome message
        if not st.session_state.processed_files:
            st.info("👈 Start by uploading documents in the sidebar!")
        else:
            st.info("💬 Ask any question about your uploaded documents below!")

if __name__ == "__main__":
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        st.error("⚠️ OpenAI API key not found! Please set it in the .env file.")
        st.stop()

    main()
