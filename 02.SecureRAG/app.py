import streamlit as st

# Import the RAG functions.
from rag_pipeline import index_files, answer_question


# PAGE CONFIGURATION

st.set_page_config(
    page_title="SecureRAG",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 SecureRAG")
st.caption("AI Document Security and Prompt Injection Defense")



# SESSION STATE
# Store chat messages during the current session.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Track whether documents have been indexed.
if "documents_indexed" not in st.session_state:
    st.session_state.documents_indexed = False



# SIDEBAR: DOCUMENT UPLOAD
with st.sidebar:

    st.title("Upload Documents")

    # Allow multiple PDF, CSV and TXT files.
    uploaded_files = st.file_uploader(
        "Choose your documents",
        type=["pdf", "csv", "txt"],
        accept_multiple_files=True
    )

    # Index uploaded documents when clicked.
    if st.button("Index Documents", use_container_width=True):

        if uploaded_files:

            with st.spinner("Loading documents and creating embeddings..."):

                try:
                    # Send uploaded files to the RAG pipeline.
                    chunk_count = index_files(uploaded_files)

                    st.session_state.documents_indexed = True

                    st.success(
                        f"Successfully indexed {chunk_count} chunks!"
                    )

                except Exception as error:
                    st.error(f"Indexing failed: {error}")

        else:
            st.warning("Please upload at least one document.")

    st.divider()

    st.caption("Supported formats: PDF, CSV and TXT")
    
    # Clear chat history
    if st.button("🗑️ Clear Chat History", use_container_width=True):

        st.session_state.messages = []

        st.rerun()

        st.divider()

    # Project introduction
    st.markdown("### 🔐 About SecureRAG")

    st.caption(
        """
        SecureRAG is an AI-powered enterprise knowledge assistant

        It uses RAG to retrieve information from
        documents while implementing security measures against
        prompt injection and malicious document content.
        """
    )

    st.caption("Built with Python, Streamlit, LangChain and Ollama.")



# DISPLAY PREVIOUS CHAT MESSAGES
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        # Display source references for assistant messages.
        if message["role"] == "assistant" and message.get("sources"):

            with st.expander("Sources used"):

                for source in message["sources"]:

                    st.write(
                        f"{source['source']} — {source['detail']}"
                    )


# USER CHAT INPUT
user_input = st.chat_input("Ask a question about your documents...")


if user_input:

    # Display and save the user's message.
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)


    # GENERATE ANSWER USING RAG
    with st.chat_message("assistant"):

        if not st.session_state.documents_indexed:

            answer = "Please upload and index your documents before asking questions."

            st.warning(answer)

            sources = []

        else:

            with st.spinner("Searching documents and generating answer..."):

                try:
                    # Retrieve relevant document chunks and generate an answer.
                    result = answer_question(user_input)

                    answer = result["answer"]
                    sources = result["sources"]

                    st.markdown(answer)

                    # Show document references.
                    if sources:

                        with st.expander("Sources used"):

                            for source in sources:

                                st.write(
                                    f"{source['source']} — {source['detail']}"
                                )

                except Exception as error:

                    answer = f"An error occurred: {error}"
                    sources = []

                    st.error(answer)


    # Save assistant response and sources in chat history.
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })
