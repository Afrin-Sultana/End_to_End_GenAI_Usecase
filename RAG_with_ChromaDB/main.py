from vector_store import VectorStore
from retrieval import RAG


if __name__ == "__main__":
    vector_store = VectorStore()
    vector_store.generate_indexing()
    rag = RAG()
    query = "What are the main problem associated with Random FOrest?"
    final_response, _ = rag.query_rag(query)
    print(final_response)
