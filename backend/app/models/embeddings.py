from langchain_community.embeddings import SentenceTransformerEmbeddings

def get_embeddings():
    return SentenceTransformerEmbeddings(
        model_name='ng3owb/sentiment-embedding-model'
    )

