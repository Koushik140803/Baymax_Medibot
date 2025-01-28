from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from transformers import T5Tokenizer, T5ForConditionalGeneration
import faiss
import numpy as np
import pandas as pd
import warnings
import os

warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Load models and data
print("Loading models and data...")

# Sentence Transformer for embeddings
embed_model = SentenceTransformer('all-mpnet-base-v2')

# Load FAISS index
faiss_index_path = "subset_knowledge_base_faiss_index.bin"
faiss_index = faiss.read_index(faiss_index_path)

# Load metadata (knowledge base)
metadata_path = "subset_knowledge_base_with_embeddings.csv"
metadata_df = pd.read_csv(metadata_path)

# Load T5 model and tokenizer for generating answers
local_model_path = r"C:\Users\Kaushik\Desktop\baymax_personal\fine_tuned_flan_t5"
tokenizer = T5Tokenizer.from_pretrained(local_model_path, local_files_only=True, legacy=True)
model = T5ForConditionalGeneration.from_pretrained(local_model_path, local_files_only=True, from_tf=True)

print("Models and data loaded successfully!")

# Helper function for summarizing lengthy contexts
def summarize_context(context: str, max_length: int = 150) -> str:
    """
    Summarizes the input context using the T5 model to make it concise.
    """
    input_text = f"Summarize: {context}"
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512)
    outputs = model.generate(inputs.input_ids, max_length=max_length, num_beams=3, temperature=0.7, early_stopping=True)
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary

# Define helper function to handle the RAG pipeline
def generate_response(query: str, top_k: int = 5):
    try:
        # Generate query embedding
        query_embedding = embed_model.encode(query, convert_to_tensor=False)

        # Search FAISS index for top-k similar entries
        distances, indices = faiss_index.search(np.array([query_embedding]), top_k)

        # Retrieve both input (question) and response (answer) from metadata
        retrieved_contexts = [
            f"Question: {metadata_df.iloc[idx]['input']}\nAnswer: {metadata_df.iloc[idx]['response']}" 
            for idx in indices[0]
        ]
        retrieved_context = "\n".join(retrieved_contexts)

        # Only summarize if context is very lengthy
        if len(retrieved_context) > 1000:  # Increased length threshold before summarization
            retrieved_context = summarize_context(retrieved_context)

        # Prepare input for T5 model
        input_text = f"Query: {query}\nContext: {retrieved_context}\nAnswer:"
        inputs = tokenizer(input_text, return_tensors="pt", max_length=1024, truncation=True)

        # Generate answer using T5 (Increased max_length and num_beams for better exploration)
        outputs = model.generate(inputs.input_ids, max_length=1024, num_beams=5, temperature=0.7, early_stopping=True)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return response, retrieved_context
    except Exception as e:
        raise RuntimeError(f"Error during response generation: {e}")

# Define endpoint for querying
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

@app.post("/query/")
async def query_endpoint(request: QueryRequest):
    """
    Endpoint to handle RAG queries.

    Parameters:
    - query (str): The query to be answered.
    - top_k (int): Number of top results to retrieve from FAISS.

    Returns:
    - response (str): The generated answer.
    - context (str): The retrieved context from the knowledge base.
    """
    try:
        response, context = generate_response(request.query, request.top_k)
        return {"response": response, "context": context}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# Root endpoint for basic server status
@app.get("/")
async def root():
    return {"message": "Welcome to the RAG-based API. Use /query/ to ask a question!"}
