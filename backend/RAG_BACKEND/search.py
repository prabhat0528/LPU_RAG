import os
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from bs4 import BeautifulSoup
from dotenv import load_dotenv


api_key = os.getenv("GEMINI_API_KEY")


url = "https://www.lpu.in/"

loader = RecursiveUrlLoader(
    url=url,
    max_depth=2,
    extractor=lambda x: BeautifulSoup(x, "html.parser").get_text(),
    timeout=100,
    continue_on_failure=True  
)

docs = loader.load()

# Spliting into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(docs)

# Embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key = api_key
)

# Store in Chroma
db = Chroma.from_documents(
    chunks,
    embedding=embeddings,
    persist_directory="vectorstore"
)

db.persist()

print("Ingestion Complete")