from langchain_chroma import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings  ## Old Version
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
import os
from config import CHROMA_PATH, EMBEDDING_MODEL_NAME
from data_processing import DataProcessing
os.environ["TOKENIZERS_PARALLELISM"] = "false"

class VectorStore:
    def __init__(self):
        self.embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        
    
    def save_to_chroma(self, chunks: list[Document]):
        if os.path.exists(CHROMA_PATH):
            db = Chroma(persist_directory=CHROMA_PATH, embedding_function=self.embedding_function)
            existing_sources = self.get_indexed_Sources_from_Chroma()
            print(f"Existing sources in Chroma DB: {existing_sources}")
            new_chunks = [chunk for chunk in chunks if chunk.metadata.get("source") not in existing_sources]
            if not new_chunks:
                print("Chroma DB already contains all documents. Skipping ingestion.")
                return
            db.add_documents(new_chunks)
            print(f"Added {len(new_chunks)} new chunks to {CHROMA_PATH}.")


        else:
            print("Chroma DB does not exist. Creating new one.")

        

    def queryChroma(self, query_text: str, k=3):
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=self.embedding_function)
        results = db.similarity_search_with_relevance_scores(query_text, k=k)
        return results
    
    def generate_indexing_for_Chroma(self,file_path: str):
        processor = DataProcessing()
        if os.path.isfile(file_path):
            documents = processor.load_single_pdf(file_path)
        elif os.path.isdir(file_path):
            documents = processor.load_pdfs_from_directory(file_path)
        else:
            raise ValueError(f"Invalid file path: {file_path}. It should be a file or a directory.")
        
        chunks = processor.create_chunks(documents)
        self.save_to_chroma(chunks)

    def get_indexed_Sources_from_Chroma(self):
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=self.embedding_function)
        collection= db._collection
        all_metadata= collection.get(include=["metadatas"])["metadatas"]
        return set(m.get("source") for m in all_metadata if m.get("source"))
        # return any(os.path.basename(m.get("source",""))==file_name for m in all_metadata)

    def is_file_name_indexed_inChroma(self, file_name: str):
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=self.embedding_function)
        collection= db._collection
        all_metadata= collection.get(include=["metadatas"])["metadatas"]
        # return set(m.get("source") for m in all_metadata if m.get("source"))
        return any(os.path.basename(m.get("source",""))==file_name for m in all_metadata)
        
