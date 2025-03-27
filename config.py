"""Configuration settings and model initialization for the chatbot."""

import os
import logging
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment variables
os.environ["GOOGLE_API_KEY"] = "Your API Key"
DOCS_DIR = "./demo_bot_data"
VECTOR_STORE_PATH = "faiss_ubuntu_docs"

# Initialize models
def initialize_models():
    """Initialize and return Gemini LLM and embeddings models."""
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        return llm, embeddings
    except Exception as e:
        logger.error(f"Bro Error in initializing models: {e}")
        raise

gemini_llm, gemini_embeddings = initialize_models()