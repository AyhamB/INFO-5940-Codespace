import streamlit as st
import os
import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains.retrieval_qa.base import RetrievalQA

# --- Page setup ---
st.set_page_config(page_title="🧠 Multi-Document RAG Chat", layout="wide")
st.title("📄 Chat with Multiple Documents (.txt + .pdf)")

# --- Hero Section: Intro card ---
st.markdown(
    """
    <div style="
        background-color:#f8f9fa;
        border-radius:15px;
        padding:20px 30px;
        margin-top:10px;
        margin-bottom:25px;
        border:1px solid #e1e4e8;
    ">
        <h3 style="color:#2b2b2b;">💡 About this App</h3>
        <p style="color:#444; font-size:16px; line-height:1.6;">
            This Retrieval-Augmented Generation (RAG) demo allows you to 
            <b>upload multiple .txt or .pdf documents</b> and 
            <b>chat interactively with their content</b>.
            It uses <b>LangChain</b> + <b>ChromaDB</b> for retrieval, and 
            <b>OpenAI models via Cornell AI Gateway</b> for generation.
        </p>
        <ul style="color:#333; font-size:15px; line-height:1.6;">
            <li>📄 Supports multiple file uploads (.txt & .pdf)</li>
            <li>🔍 Performs chunking, embedding, and semantic retrieval</li>
            <li>💬 Provides a chat-style interface with source citations</li>
        </ul>
        <p style="color:#555; font-size:15px; margin-top:10px;">
            Built as part of <b>INFO 5940 – Applied AI Systems Design</b>.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Sidebar: App Info and Controls ---
st.sidebar.header("⚙️ Controls")
st.sidebar.markdown(
    """
**Instructions**
1. Upload one or more `.txt` or `.pdf` files.  
2. Ask a question about their content in the chat box below.  
3. The assistant will retrieve and summarize from all uploaded files.
    """
)

# Clear chat button
if st.sidebar.button("🧹 Clear Chat History"):
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Chat cleared. Upload files and ask again!"}
    ]
    st.rerun()

# --- Chat session initialization ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Upload one or more documents and ask me anything about them."}
    ]

# --- File uploader section ---
uploaded_files = st.file_uploader(
    "📂 Upload your .txt or .pdf files here:",
    type=["txt", "pdf"],
    accept_multiple_files=True
)

# Display uploaded file list
if uploaded_files:
    st.sidebar.subheader("📁 Uploaded Files")
    for f in uploaded_files:
        st.sidebar.write(f"- {f.name}")

# --- Display chat history ---
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


# --- Function: build vectorstore from uploaded files ---
def build_vectorstore_from_files(files):
    """
    Reads and processes multiple files (.txt and .pdf),
    splits them into chunks, generates embeddings,
    and stores them in a Chroma vector database.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts, metadatas = [], []

    # Show progress bar while processing files
    progress_bar = st.progress(0, text="Processing uploaded documents...")
    total_files = len(files)

    for idx, file in enumerate(files):
        filename = file.name
        text = ""

        # Handle text files
        if filename.lower().endswith(".txt"):
            text = file.read().decode("utf-8")

        # Handle PDF files
        elif filename.lower().endswith(".pdf"):
            try:
                with pdfplumber.open(file) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            except Exception as e:
                st.error(f"❌ Error reading {filename}: {e}")
                continue

        if not text.strip():
            st.warning(f"⚠️ No text extracted from {filename}")
            continue

        # Split into chunks and tag with metadata
        chunks = splitter.split_text(text)
        texts.extend(chunks)
        metadatas.extend([{"source": filename}] * len(chunks))

        progress_bar.progress((idx + 1) / total_files, text=f"Indexed: {filename}")

    progress_bar.empty()  # Remove the bar once done

    # --- Embedding model (Cornell Gateway) ---
    embeddings = OpenAIEmbeddings(
        model="openai.text-embedding-3-small",
        api_key=os.environ["API_KEY"],
        base_url="https://api.ai.it.cornell.edu",
        dimensions=1536
    )

    # --- Build Chroma vectorstore ---
    vectorstore = Chroma.from_texts(texts, embedding=embeddings, metadatas=metadatas)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return retriever


# --- Chat input box ---
question = st.chat_input("💬 Ask something about your uploaded files...", disabled=not uploaded_files)

# --- Handle user queries ---
if question and uploaded_files:
    with st.spinner("🔍 Building document index and retrieving information..."):
        retriever = build_vectorstore_from_files(uploaded_files)

    # Initialize LLM (Cornell Gateway)
    llm = ChatOpenAI(
        model_name="openai.gpt-4o-mini",
        api_key=os.environ["API_KEY"],
        base_url="https://api.ai.it.cornell.edu"
    )

    # Create Retrieval-Augmented Generation (RAG) chain
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True  # Return document references
    )

    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    # Generate assistant response
    with st.chat_message("assistant"):
        result = qa.invoke({"query": question})
        answer = result["result"]
        sources = list({doc.metadata["source"] for doc in result["source_documents"]})
        st.write(answer)
        if sources:
            st.caption(f"🗂 Sources: {', '.join(sources)}")

    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": answer})
