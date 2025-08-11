from langchain_community.vectorstores import Chroma
from app.models.embeddings import get_embeddings
from app.config import VECTOR_DB_DIR

def save_to_vector_store(documents):
    embeddings = get_embeddings()
    vector_store = Chroma.from_documents(
        documents, embeddings, persist_directory=VECTOR_DB_DIR
    )
    vector_store.persist()

def load_vector_store():
    embeddings = get_embeddings()
    return Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)
