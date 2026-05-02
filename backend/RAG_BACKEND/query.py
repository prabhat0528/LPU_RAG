from flask import Flask, request, jsonify
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

import os
from dotenv import load_dotenv
api_key = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)

# Load embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=api_key
)

# Load vector DB
db = Chroma(
    persist_directory="vectorstore",
    embedding_function=embeddings
)

retriever = db.as_retriever(search_kwargs={"k": 4})

# Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0 ,
    google_api_key = api_key
)

#  Strict prompt
prompt_template = """
You are an assistant answering questions ONLY from the provided context.

RULES:
- If answer is NOT in context just say "I don't know based on the provided data."
- Do NOT make up answers
- Be precise and factual

Context:
{context}

Question:
{question}

Answer:
"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": PROMPT}
)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query missing"}), 400

    response = qa_chain.run(query)

    return jsonify({
        "query": query,
        "answer": response
    })

if __name__ == "__main__":
    app.run(debug=True)