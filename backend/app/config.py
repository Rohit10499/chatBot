import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
VECTOR_DB_DIR = os.getenv("VECTOR_DB_DIR", "./vector_db")

