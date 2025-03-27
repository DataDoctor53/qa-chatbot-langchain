from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
import uvicorn
import logging
import os

# Resolve OpenMP runtime issue
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# Import your configuration and helper modules
from config import gemini_llm, gemini_embeddings, VECTOR_STORE_PATH
from vector_store import load_vector_store
from con_qa_chain import create_qa_chain

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler for startup/shutdown events"""
    try:
        # Startup initialization
        logger.info("Loading vector store")
        app.vector_store = load_vector_store(VECTOR_STORE_PATH, gemini_embeddings)
        app.retriever = app.vector_store.as_retriever(search_kwargs={"k": 5})
        logger.info("Creating QA chain")
        app.qa_chain = create_qa_chain(gemini_llm, app.retriever)
        yield
    except Exception as e:
        logger.error(f"Startup initialization error: {str(e)}")
        raise RuntimeError(f"Failed to initialize application: {str(e)}")
    finally:
        # Cleanup resources if needed
        pass

app = FastAPI(
    title="Ubuntu Documentation Chatbot",
    version="1.0.0",
    lifespan=lifespan
)

# Enhanced CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    allow_credentials=True,
)

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@app.get("/")
async def health_check():
    return {
        "status": "running",
        "api_docs": "/docs",
        "interactive_docs": "/redoc"
    }

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """Endpoint for submitting questions to the chatbot."""
    try:
        logger.info(f"Processing question: {request.question}")
        # Use ainvoke instead of deprecated acall
        result = await app.qa_chain.ainvoke({
            "question": request.question,
            "chat_history": []  # Initialize empty chat history
        })
        
        if "answer" not in result:
            logger.error("Invalid response format from QA chain")
            raise HTTPException(500, "Invalid response from AI model")
            
        logger.info(f"Response generated: {result['answer'][:50]}...")
        return QueryResponse(answer=result["answer"])
        
    except KeyError as e:
        logger.error(f"Missing key in response: {str(e)}")
        raise HTTPException(500, "Invalid response format from AI model")
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(500, f"Chatbot error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False
    )