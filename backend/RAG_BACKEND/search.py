import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

# Load env variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# ----------- LOAD PDF -----------
pdf_loader = PyPDFLoader("Lovely Professional University.pdf")
docs = pdf_loader.load()

# ----------- SPLITTING -----------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=50
)

chunks = splitter.split_documents(docs)

# ----------- EMBEDDINGS -----------
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=api_key
)

# ----------- VECTOR STORE -----------
db = Chroma.from_documents(
    chunks,
    embedding=embeddings,
    persist_directory="vectorstore"
)

db.persist()

print(f"Ingestion Complete | Total Chunks: {len(chunks)}")