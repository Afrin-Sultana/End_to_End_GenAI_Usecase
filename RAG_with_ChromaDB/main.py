import os
from dotenv import load_dotenv
from data_processing import DataProcessing
from vector_store import VectorStore
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from config import PDF_DIRECTORY

load_dotenv()
api_key = os.getenv("OPEN_AI_KEY")

def generate_data_store():
    processor = DataProcessing(pdf_directory=PDF_DIRECTORY)
    documents = processor.load_pdfs()
    chunks = processor.create_chunks(documents)

    vector_store = VectorStore()
    vector_store.save_to_chroma(chunks)

def query_rag(query_text: str):
    vector_store = VectorStore()
    results = vector_store.query(query_text, k=3)

    if not results:
        return "No relevant documents found.", []

    context_text = "\n\n - -\n\n".join([doc.page_content for doc, _ in results])
    sources = [f"{doc.metadata.get('source', 'Unknown')} (page {doc.metadata.get('page', 'N/A')})" for doc, _ in results]

    prompt_template = ChatPromptTemplate.from_template(
        "You have the following context: {context}.\nAnswer the question: {question}"
    )
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=api_key)
    messages = [SystemMessage(content="You are a helpful assistant."), HumanMessage(content=prompt)]
    response = model.invoke(messages)

    return f"Response: {response}\nSources: {sources}", response

if __name__ == "__main__":
    generate_data_store()
    query = "Explain Random Forest algorithm in detail."
    final_response, _ = query_rag(query)
    print(final_response)
