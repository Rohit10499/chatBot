from fastapi import APIRouter, UploadFile
import os
import shutil
from app.services.document_processor import load_document
from app.utils.chunking import chunk_documents
from app.models.vector_store import save_to_vector_store

router = APIRouter()

@router.post("/upload")
async def upload_documents(files: list[UploadFile]):
    upload_dir = "./uploads"
    os.makedirs(upload_dir, exist_ok=True)  
    all_chunks = []

    for file in files:
        file_path = os.path.join(upload_dir, file.filename)

     
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

      
        docs = load_document(file_path)
        chunks = chunk_documents(docs)
        all_chunks.extend(chunks)  

    
    save_to_vector_store(all_chunks)

    return {"message": f"{len(files)} files indexed successfully"}

