# 🧠 INFO 5940 — Assignment 1: Multi-Document RAG Chat

Welcome to my **INFO 5940 Assignment 1** submission!  
This project implements a **Retrieval-Augmented Generation (RAG)** app using **Streamlit**, **LangChain**, and **Chroma**.  
It allows users to upload multiple `.txt` and `.pdf` files, ask natural-language questions, and receive accurate answers grounded in the uploaded documents.

---

## 🚀 Features
- 📄 Upload multiple `.txt` and `.pdf` documents  
- 🔍 Automatic document chunking for large files  
- 🧩 Embedding with **`openai.text-embedding-3-small`** stored in a **Chroma vector database**  
- 💬 Conversational Streamlit interface supporting multi-turn dialogue  
- 🔒 Secure API-key management with `.env` / `.env.sample`  
- 🧠 Answer generation via **`openai.gpt-4o-mini`**

---

## 🛠️ Setup Instructions (inside GitHub Codespaces)

### Step 1 — Open Codespace
1. Go to your forked repo on GitHub.  
2. Click **Code → Codespaces → Open Codespace on `assignment1`**.  
3. Wait for the environment to finish setting up.  

---

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt