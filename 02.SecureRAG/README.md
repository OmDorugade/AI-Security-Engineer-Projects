# 🔐 SecureRAG — AI Document Security & Prompt Injection Defense

SecureRAG is a locally hosted AI-powered document assistant built using Retrieval-Augmented Generation (RAG).   
The project mainly focuses on detecting direct and indirect prompt injection attacks in user inputs and uploaded documents.  
It also implements document security checks and trust boundaries to make RAG applications more security-aware.

Users can upload their own PDF, CSV, or TXT documents and ask questions about their content — it is not limited to HR or IT documents.
The project focuses on detecting direct and indirect prompt injection attacks and implementing security mechanisms for RAG applications.

## 🎯 Project Objectives

- Build a local Retrieval-Augmented Generation (RAG) application.
- Detect suspicious instructions in user prompts.
- Scan uploaded documents for potential indirect prompt injection.
- Reject documents containing detected malicious instructions.
- Establish trust boundaries between document content and system instructions.
- Inspect retrieval scores to understand document relevance.

## 🛡️ Security Features

- **Direct Prompt Injection Detection:** Detects suspicious user prompts containing known instruction-override patterns and blocks them before retrieval and LLM processing.
- **Indirect Prompt Injection Detection:** Scans uploaded document content for potentially malicious instructions.
- **Malicious Document Handling:** Excludes flagged document pages or rows from indexing and removes previously indexed content when an entire uploaded file is rejected.
- **Document Trust Boundary:** Instructs the LLM to treat retrieved document content as untrusted evidence rather than instructions to follow.
- **Retrieval Score Inspection:** Displays distance scores for retrieved documents to help evaluate retrieval relevance.

## ⚙️ Technology Stack

- **Language:** Python
- **Frontend:** Streamlit
- **LLM:** Llama 3.1 (8B) through Ollama
- **Embeddings:** mxbai-embed-large
- **Vector Database:** ChromaDB
- **RAG Framework:** LangChain
- **Document Processing:** PyPDF, CSV and TXT loaders
- **Security Detection:** Python Regular Expressions

## 🏗️ System Design

```text

                                     ┌──────────────────────────┐
                                     │       User Interface     │
                                     │         Streamlit        │
                                     └────────────┬─────────────┘
                                                  │
                                     ┌────────────▼─────────────┐
                                     │       User Request       │
                                     │  Upload / Ask Question   │
                                     └────────────┬─────────────┘
                                                  │
                                     ┌────────────▼─────────────┐
                                     │      Security Layer      │
                                     │                          │
                                     │  Direct Injection Scan   │
                                     │  Indirect Injection Scan  │
                                     │  Document Security       │
                                     └────────────┬─────────────┘
                                                  │
                                     ┌────────────▼─────────────┐
                                     │       RAG Pipeline       │
                                     │                          │
                                     │  Document Processing     │
                                     │  Text Splitting          │
                                     │  Embedding & Retrieval   │
                                     └────────────┬─────────────┘
                                                  │
                                     ┌────────────▼─────────────┐
                                     │        ChromaDB          │
                                     │      Vector Store        │
                                     └────────────┬─────────────┘
                                                  │
                                     ┌────────────▼─────────────┐
                                     │        Ollama LLM        │
                                     │        Llama 3.1         │
                                     │                          │
                                     │  Untrusted Document      │
                                     │  Context + User Query    │
                                     └────────────┬─────────────┘
                                                  │
                                     ┌────────────▼─────────────┐
                                     │     Generated Answer     │
                                     │   + Document Sources     │
                                     └──────────────────────────┘
```

**Architecture Components:**
- **Streamlit:** Handles document uploads and user queries.
- **Security Layer:** Checks user prompts and uploaded documents for suspicious instructions.
- **RAG Pipeline:** Processes documents, generates embeddings, and retrieves relevant content.
- **ChromaDB:** Stores document embeddings for similarity-based retrieval.
- **Ollama + Llama 3.1:** Generates answers using retrieved document context treated as untrusted evidence.

## 📚 Key Learnings

- Understanding RAG architecture and vector databases.
- Implementing direct and indirect prompt injection detection.
- Handling malicious documents during the indexing process.
- Applying trust boundaries to retrieved document context.
- Understanding security challenges in LLM-powered applications.

## ⚠️ Disclaimer

SecureRAG is an educational defensive prototype. Its regex-based detection and prompt-level protections do not guarantee detection or prevention of every prompt injection attack. Retrieval score inspection is available for analysis, but automatic relevance-threshold filtering is not activated.

## Result


