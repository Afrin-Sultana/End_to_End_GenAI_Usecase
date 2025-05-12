from langchain_chroma import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings  ## Old Version
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
import os
from config import CHROMA_PATH, EMBEDDING_MODEL_NAME

class VectorStore:
    def __init__(self):
        self.embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    def save_to_chroma(self, chunks: list[Document]):
        if os.path.exists(CHROMA_PATH):
            db = Chroma(persist_directory=CHROMA_PATH, embedding_function=self.embedding_function)
            if db._collection.count() > 0:
                print("Chroma DB already populated.")
                return
            print("Chroma DB exists but is empty. Populating.")
        else:
            print("Chroma DB does not exist. Creating new one.")

        db = Chroma.from_documents(chunks, self.embedding_function, persist_directory=CHROMA_PATH)
        print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

    def query(self, query_text: str, k=3):
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=self.embedding_function)
        results = db.similarity_search_with_relevance_scores(query_text, k=k)
        return results
