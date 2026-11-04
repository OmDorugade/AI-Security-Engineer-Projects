from langchain_ollama import OllamaEmbeddings

#embedding model from ollama 
def get_embeddings():
    return OllamaEmbeddings(
        model="mxbai-embed-large"
    )



