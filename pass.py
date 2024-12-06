import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from azure.ai.openai import OpenAIClient
from azure.core.credentials import AzureKeyCredential
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from pydantic import BaseModel
from typing import Optional
import uuid
import datetime

# Initialize FastAPI app
app = FastAPI()

# Static and templates setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load environment variables
load_dotenv()
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
CHROMA_DB_PATH = "chromadb"  # Path where your ChromaDB is stored

# Initialize Azure OpenAI client
openai_client = OpenAIClient(
    endpoint=AZURE_OPENAI_ENDPOINT,
    credential=AzureKeyCredential(AZURE_OPENAI_KEY)
)

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory storage
documents = {}
conversation_history = {}

# Initialize vector database
vectordb = None


def initialize_vector_db():
    global vectordb
    if vectordb is None:
        vectordb = Chroma(
            embedding_function=lambda texts: get_embeddings(texts),
            persist_directory=CHROMA_DB_PATH
        )
    return vectordb


def get_embeddings(texts):
    """Fetch embeddings using Azure OpenAI."""
    response = openai_client.get_embeddings(
        deployment_id="test-embedding-3-small",  # Azure OpenAI embedding deployment
        input=texts
    )
    return [item["embedding"] for item in response["data"]]


initialize_vector_db()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the upload page."""
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse)
async def handle_upload(request: Request, document: UploadFile = File(...)):
    """Handle PDF upload and process the document."""
    if document.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    file_path = os.path.join(UPLOAD_FOLDER, document.filename)
    with open(file_path, "wb") as f:
        f.write(await document.read())

    try:
        # Read PDF content
        from PyPDF2 import PdfReader
        reader = PdfReader(file_path)
        content = "\n".join([page.extract_text() for page in reader.pages])

        # Split text and add to vector DB
        chunks = [content[i:i+1000] for i in range(0, len(content), 1000)]
        vectordb.add_texts(
            texts=chunks,
            ids=[f"{document.filename}-{i}" for i in range(len(chunks))]
        )

        vectordb.persist()

        doc_id = len(documents) + 1
        documents[doc_id] = document.filename

        return templates.TemplateResponse("chat.html", {"request": request, "doc_id": doc_id})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chat/{doc_id}", response_class=HTMLResponse)
async def chat(doc_id: int, request: Request):
    """Render the chat page."""
    if doc_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")
    return templates.TemplateResponse("chat.html", {"request": request, "doc_id": doc_id})


class ChatRequest(BaseModel):
    query: str


@app.post("/interact/{doc_id}")
async def interact_with_document(doc_id: int, chat_request: ChatRequest):
    """Handle chat interactions."""
    if doc_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")

    user_query = chat_request.query
    search_results = vectordb.similarity_search_with_score(user_query, k=5)
    relevant_content = "\n".join([result[0] for result in search_results])

    history = conversation_history.get(doc_id, "")

    # Define the prompt
    prompt = (
        "You are a helpful assistant.\n"
        "Conversation history:\n{history}\n"
        "Relevant document content:\n{relevant_content}\n"
        "User query: {user_query}\n"
        "Always respond based on the context provided."
    ).format(history=history, relevant_content=relevant_content, user_query=user_query)

    # Generate a response using Azure OpenAI
    try:
        response = openai_client.get_chat_completion(
            deployment_id="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=800,
            temperature=0.7,
        )
        reply = response["choices"][0]["message"]["content"]

        # Update conversation history
        conversation_history[doc_id] = history + f"User: {user_query}\nAssistant: {reply}\n"

        return JSONResponse(content={"response": reply})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
#######################################################################################



from azure.ai.openai import OpenAIClient
from azure.core.credentials import AzureKeyCredential

# Configuration
AZURE_OPENAI_KEY = "your-azure-openai-api-key"
AZURE_OPENAI_ENDPOINT = "https://your-azure-openai-endpoint.openai.azure.com"
EMBEDDING_DEPLOYMENT_ID = "test-embedding-3-small"  # Replace with your deployment ID

# Initialize OpenAI client
client = OpenAIClient(
    endpoint=AZURE_OPENAI_ENDPOINT,
    credential=AzureKeyCredential(AZURE_OPENAI_KEY)
)

# Text for which you want to generate embeddings
input_text = "Hello, how are you?"

# Fetch embeddings
try:
    response = client.get_embeddings(
        deployment_id=EMBEDDING_DEPLOYMENT_ID,
        input=input_text
    )
    embeddings = response["data"][0]["embedding"]
    print(f"Embedding for '{input_text}':\n{embeddings[:10]}...")  # Print the first 10 values
    print(f"Embedding length: {len(embeddings)}")
except Exception as e:
    print(f"Error fetching embeddings: {e}")

