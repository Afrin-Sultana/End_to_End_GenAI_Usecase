# Langchain dependencies
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.chat_models import ChatOpenAI 
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain.schema import Document 
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
import os 
import shutil 
from dotenv import load_dotenv 

# Load environment variables from .env file
load_dotenv()
# Set OpenAI API key
api_key = os.getenv("OPEN_AI_KEY")
os.environ["TOKENIZERS_PARALLELISM"] = "false"

pdf_directory = "Data"  # Define the directory containing the PDF files

## Step 1: Load PDF files
def load_pdfs(pdf_directory):
    if not os.path.exists(pdf_directory):
        print(f"Directory does not exist: {pdf_directory}")
    else:
        print("PDF files found:", os.listdir(pdf_directory))
        loader = PyPDFDirectoryLoader(pdf_directory)
        return loader.load()

# documents = load_pdfs(pdf_directory) # Load the documents
# print(documents[0])


## Step 2: Split text into smaller chunks
def split_text(documents: list[Document]):
  """
  Split the text content of the given list of Document objects into smaller chunks.
  Args:
    documents (list[Document]): List of Document objects containing text content to split.
  Returns:
    list[Document]: List of Document objects representing the split text chunks.
  """
  # Initialize text splitter with specified parameters
  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800, # Size of each chunk in characters
    chunk_overlap=100, # Overlap between consecutive chunks
    length_function=len, # Function to compute the length of the text
    add_start_index=True, # Flag to add start index to each chunk
  )

  # Split documents into smaller chunks using text splitter
  chunks = text_splitter.split_documents(documents)
  print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

  # Print example of page content and metadata for a chunk
  document = chunks[0]
#   print(document.page_content)
  print("Example Metadata")
  print(document.metadata)

  return chunks # Return the list of split text chunks



# Load a pre-trained SentenceTransformer model
embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")



# Path to the directory to save Chroma database
CHROMA_PATH = "chroma"
def save_to_chroma(chunks: list[Document], ):
    if os.path.exists(CHROMA_PATH):
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
        existing_docs = db._collection.count()
        
        if existing_docs > 0:
            print(f"Chroma DB already contains {existing_docs} documents. Skipping ingestion.")
            return
        else:
            print("Chroma DB exists but is empty. Proceeding to populate.")

    else:
        print("Chroma DB does not exist. Creating new one.")

    db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=CHROMA_PATH
    )
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")





def generate_data_store():
  """
  Function to generate vector database in chroma from documents.
  """
  documents = load_pdfs(pdf_directory) # Load documents from a source
  chunks = split_text(documents) # Split documents into manageable chunks
  save_to_chroma(chunks) # Save the processed data to a data store


generate_data_store()


query_text = "Explain Random Forest algorithm in detail."


def query_rag(query_text):
 
  # YOU MUST - Use same embedding function as before
  embedding_function = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")

  # Prepare the database
  db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
  
  # Retrieving the context from the DB using similarity search
  results = db.similarity_search_with_relevance_scores(query_text, k=3)

#   # Check if there are any matching results or if the relevance score is too low
#   if len(results) == 0 or results[0][1] < 0.7:
#     print(f"Unable to find matching results.")

  # Combine context from matching documents
  context_text = "\n\n - -\n\n".join([doc.page_content for doc, _score in results])
#   print(f"Context:\n {context_text}")
  PROMPT_TEMPLATE = """You have got the following context: {context}.
                       Answer the question based on the above context: {question}"""
 
  ## Create prompt template using context and query text
  prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
  prompt = prompt_template.format(context=context_text, question=query_text)
  
  # Initialize OpenAI chat model
  model = ChatOpenAI(model="gpt-4o", 
                     temperature=0, 
                     openai_api_key=api_key)

  # Generate response text based on the prompt
  messages = [
             SystemMessage(content="You are a helpful assistant."),
             HumanMessage(content=prompt)
         ]
  response_text = model.invoke(messages)

 
   # Get sources of the matching documents
  sources = [ f"{doc.metadata.get('source', 'Unknown source')} (page {doc.metadata.get('page', 'N/A')})" for doc, _score in results]
 
  # Format and return response including generated text and sources
  formatted_response = f"Response: {response_text}\nSources: {sources}"
  return formatted_response, response_text

# Let's call our function we have defined
formatted_response, response_text = query_rag(query_text)
# and finally, inspect our final response!
print("Here is the final response:\n")
print(formatted_response)