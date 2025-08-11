from langchain_community.document_loaders import PyPDFLoader

def load_document(file_path: str):
    if file_path.lower().endswith(".pdf"):
        loader = PyPDFLoader(file_path)
        return loader.load()
    else:
        raise ValueError("Unsupported file format")