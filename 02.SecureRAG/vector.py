from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

from embeddings import get_embeddings

# Store the vector database inside our project folder
DB_DIRECTORY = str(
    Path(__file__).parent / "chroma_db"
)

COLLECTION_NAME = "securerag_documents"

def get_vector_store():

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=DB_DIRECTORY
    )

def add_documents(documents: list[Document]):
    """Replace previously indexed chunks from the same filenames."""

    if not documents:
        return 0

    store = get_vector_store()

    # Collect filenames so re-uploading a file doesn't leave its old
    # chunks mixed with the newly uploaded version.
    filenames = {
        document.metadata["source"]
        for document in documents
    }

    # Delete old chunks for these filenames only.
    for filename in filenames:
        store.delete(
            where={"source": filename}
        )

    # ChromaDB stores the text, metadata, and generated embeddings.
    store.add_documents(documents=documents)

    return len(documents)


def retrieve_documents(question, k=4):
    """Find the top-k chunks most similar to the question."""

    store = get_vector_store()

    return store.similarity_search_with_score(
        question,
        k=k,
    )



