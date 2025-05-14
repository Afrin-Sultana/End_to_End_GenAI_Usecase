from fastapi import FastAPI, UploadFile, File
from retrieval import RAG
from vector_store import VectorStore


app = FastAPI()
rag = RAG()
vector_store = VectorStore()

@app.get("/")
def read_root():
    return {"Welcome to the Q&A RAG"}

@app.get("/query")
def query_rag(query_text: str):
    response, _ = rag.query_rag(query_text)
    return {"Response": response}

@app.post("/upload-data")
def upload_data(file: UploadFile= File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are supported."}
    if vector_store.is_file_name_indexed_inChroma(file.filename):
        return {"message": f"{file.filename} is already indexed in Chroma."}
    vector_store.generate_indexing_for_Chroma()
    return {"message": f"{file.filename} has been indexed in Chroma."}

    

