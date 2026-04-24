# backend/app/services/retriever.py

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

embedding = OpenAIEmbeddings()

db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding
)

def add_documents(texts: list[str]):
    db.add_texts(texts)

def retrieve_context(query: str) -> str:
    docs = db.similarity_search(query, k=3)
    return "\n".join([d.page_content for d in docs])

