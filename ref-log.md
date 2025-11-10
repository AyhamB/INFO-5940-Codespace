# Reference Log

## Libraries and Frameworks

### Core Technologies

1. **Streamlit** (v1.36+)
   - Purpose: Web application framework for building the chat interface
   - Documentation: https://docs.streamlit.io/
   - Usage: Main UI framework, file upload, chat interface components

2. **LangChain** (v0.2.15)
   - Purpose: Framework for building RAG pipeline
   - Documentation: https://python.langchain.com/docs/
   - Usage: Document processing, text splitting, conversational retrieval chain
   - Specific modules used:
     - `langchain.text_splitter.RecursiveCharacterTextSplitter`
     - `langchain.chains.ConversationalRetrievalChain`
     - `langchain.memory.ConversationBufferMemory`

3. **LangChain OpenAI** (v0.1.23)
   - Purpose: OpenAI integration for LangChain
   - Documentation: https://python.langchain.com/docs/integrations/platforms/openai
   - Usage: OpenAI embeddings and chat model integration
   - Components: `OpenAIEmbeddings`, `ChatOpenAI`

4. **LangChain Community** (v0.2.15)
   - Purpose: Community-contributed LangChain integrations
   - Documentation: https://python.langchain.com/docs/integrations/vectorstores/chroma
   - Usage: ChromaDB vector store integration

5. **ChromaDB**
   - Purpose: Vector database for storing and retrieving document embeddings
   - Documentation: https://docs.trychroma.com/
   - Usage: Persistent vector storage, similarity search

6. **PyPDF**
   - Purpose: PDF file processing
   - Documentation: https://pypdf.readthedocs.io/
   - Usage: Extracting text content from PDF files

7. **OpenAI API** (v1.14)
   - Purpose: Language model and embeddings provider
   - Documentation: https://platform.openai.com/docs/
   - Models used:
     - `gpt-3.5-turbo`: For generating conversational responses
     - `text-embedding-ada-002`: For creating document embeddings

8. **python-dotenv**
   - Purpose: Environment variable management
   - Documentation: https://pypi.org/project/python-dotenv/
   - Usage: Loading API keys from .env file

---

## Documentation and Learning Resources

1. **LangChain RAG Tutorial**
   - URL: https://python.langchain.com/docs/tutorials/rag/
   - Usage: Understanding RAG pipeline implementation

2. **Streamlit Documentation - Chat Elements**
   - URL: https://docs.streamlit.io/develop/api-reference/chat
   - Usage: Implementing chat interface components

3. **ChromaDB Getting Started Guide**
   - URL: https://docs.trychroma.com/getting-started
   - Usage: Setting up vector store and persistence

4. **LangChain Text Splitters**
   - URL: https://python.langchain.com/docs/modules/data_connection/document_transformers/
   - Usage: Understanding chunking strategies

---

