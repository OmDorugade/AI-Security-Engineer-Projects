from langchain_text_splitters import RecursiveCharacterTextSplitter

#Long documents need to be divided into smaller chunks before embedding
def split_documents(documents):
    spliter=RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        add_start_index=True
    )

    return spliter.split_documents(documents)




