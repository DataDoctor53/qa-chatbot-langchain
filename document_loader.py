"""Module for loading and processing documentation files."""

import logging
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import MarkdownTextSplitter

logger = logging.getLogger(__name__)

def load_documents(directory_path: str):
    """Load markdown documents from specified directory."""
    try:
        logger.info(f"Loading documents from {directory_path}")
        loader = DirectoryLoader(directory_path, glob="**/*.md")
        return loader.load()
    except Exception as e:
        logger.error(f"Error loading documents: {e}")
        raise

def split_documents(documents, chunk_size=3000, chunk_overlap=300):
    """Split documents using markdown text splitter."""
    try:
        logger.info("Splitting documents into chunks")
        splitter = MarkdownTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunks = []
        for doc in documents:
            chunks.extend(splitter.split_documents([doc]))
        return chunks
    except Exception as e:
        logger.error(f"Error splitting documents: {e}")
        raise