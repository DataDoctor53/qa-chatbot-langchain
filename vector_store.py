"""Module for vector store creation and management."""

import logging
from langchain_community.vectorstores import FAISS

logger = logging.getLogger(__name__)

def create_vector_store(documents, embeddings):
    """Create and return FAISS vector store from documents."""
    try:
        logger.info("Creating vector store")
        return FAISS.from_documents(documents, embeddings)
    except Exception as e:
        logger.error(f"Error creating vector store: {e}")
        raise

def save_vector_store(vector_store, path):
    """Save vector store to disk."""
    try:
        logger.info(f"Saving vector store to {path}")
        vector_store.save_local(path)
    except Exception as e:
        logger.error(f"Error saving vector store: {e}")
        raise

def load_vector_store(path, embeddings):
    """Load vector store from disk."""
    try:
        logger.info(f"Loading vector store from {path}")
        return FAISS.load_local(path, embeddings,allow_dangerous_deserialization =True)
    except Exception as e:
        logger.error(f"Error loading vector store: {e}")
        raise