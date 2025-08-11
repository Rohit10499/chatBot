from fastapi import FastAPI
from app.routes import document_routes, query_routes,health_check

app = FastAPI(title="RAG Study Chatbot Backend")

app.include_router(health_check.router)
app.include_router(document_routes.router)
app.include_router(query_routes.router)
