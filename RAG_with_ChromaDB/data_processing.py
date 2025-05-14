from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os

class DataProcessing:
    # def __init__(self, pdf_directory: str):
    #     self.pdf_directory = pdf_directory

    def load_pdfs(self, pdf_directory) -> list[Document]:
        if not os.path.exists(pdf_directory):
            raise FileNotFoundError(f"Directory does not exist: {pdf_directory}")
        loader = PyPDFDirectoryLoader(pdf_directory)
        return loader.load()

    def create_chunks(self, documents: list[Document]) -> list[Document]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100,
            length_function=len,
            add_start_index=True
        )
        chunks = splitter.split_documents(documents)
        print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
        return chunks
