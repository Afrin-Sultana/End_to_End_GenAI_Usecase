from fastapi import FastAPI, UploadFile, File
from retrieval import RAG
from vector_store import VectorStore
import os
import shutil

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
    

    #Save the uploaded file temporarily to the Temp directory
    temp_dir = "./Temp"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, file.filename)
    with open(temp_file_path, "wb") as temp_file:
        # temp_file.write(file.file.read())
        shutil.copyfileobj(file.file, temp_file)
    

    # Generate the index for the uploaded file
    vector_store.generate_indexing_for_Chroma(temp_file_path)

    return {"message": f"{file.filename} has been indexed in Chroma."}

    

