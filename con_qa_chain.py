"""Module for conversational QA chain setup."""


import logging
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory 

logger = logging.getLogger(__name__)

def create_qa_chain(llm, retriever):
    """Create and return conversational QA chain."""
    try:
        logger.info("Initializing QA chain")
        memory = ConversationBufferWindowMemory(
            k=5,
            return_messages=True,
            memory_key="chat_history",
            output_key="answer",
            input_key="question"
        )
        
        return ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=memory,
            return_source_documents=True,
            max_tokens_limit=4096,
            chain_type="stuff",
            get_chat_history=lambda h: "\n".join([f"{m.type}: {m.content}" for m in h]),
            rephrase_question=False
        )
    except Exception as e:
        logger.error(f"Error creating QA chain: {e}")
        raise