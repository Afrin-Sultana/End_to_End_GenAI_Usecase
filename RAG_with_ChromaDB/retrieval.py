from vector_store import VectorStore
import os
from dotenv import load_dotenv
from langchain.schema import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()
api_key = os.getenv("OPEN_AI_KEY")

class RAG:
    def __init__(self):
        self.vector_store = VectorStore()

    def query_rag(self, query_text: str):
        results = self.vector_store.queryChroma(query_text, k=3)

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