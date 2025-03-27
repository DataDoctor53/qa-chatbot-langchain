"""local app"""

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
os.environ['OMP_NUM_THREADS'] = '1'  
import asyncio

from config import gemini_llm, gemini_embeddings, VECTOR_STORE_PATH
from vector_store import load_vector_store
from con_qa_chain import create_qa_chain

def initialize_resources():
    """Initialize vector store and QA chain synchronously"""
    print("Loading vector store...")
    vector_store = load_vector_store(VECTOR_STORE_PATH, gemini_embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    print("Creating QA chain...")
    return create_qa_chain(gemini_llm, retriever)

async def async_input(prompt: str) -> str:
    """Helper for async input handling"""
    return await asyncio.get_event_loop().run_in_executor(None, input, prompt)

async def chat_session(qa_chain):
    """Handle the chat session with async I/O"""
    print("\nStarting new conversation...")
    while True:
        try:
            question = await async_input("\nQuestion: ")
            if not question.strip():
                continue
                
            # Process question
            response = await qa_chain.ainvoke({
                "question": question,
                "chat_history": []
            })
            
            print(f"\nAnswer: {response.get('answer', 'No answer found')}")
            
            # Handle continuation prompt
            while True:
                choice = (await async_input(
                    "\nStart new, continue or stop? (start/continue/stop): "
                )).lower().strip()
                
                if choice in ('start', 'continue', 'stop'):
                    break
                print("Invalid choice. Please enter start/continue/stop")
                
            if choice == 'stop':
                return False
            if choice == 'start':
                return True
                
        except KeyboardInterrupt:
            return False
        except Exception as e:
            print(f"Error: {str(e)}")
            return True

async def main():
    """Main entry point for the chatbot"""
    qa_chain = initialize_resources()
    print("\nDemo Bot initialized. Press Ctrl+C to exit at any time.")
    
    try:
        while True:
            start_new = await chat_session(qa_chain)
            if not start_new:
                break
            print("\n" + "="*50 + "\n")
    except KeyboardInterrupt:
        print("\n\nExiting...")
    finally:
        print("Chat session ended")

if __name__ == "__main__":
    asyncio.run(main())