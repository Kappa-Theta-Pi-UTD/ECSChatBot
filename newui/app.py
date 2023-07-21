import os
from llama_index.callbacks.base import CallbackManager
from llama_index import (
    LLMPredictor,
    ServiceContext,
    StorageContext,
    SimpleDirectoryReader,
    load_index_from_storage,
)
from langchain.chat_models import ChatOpenAI
import openai

import chainlit as cl

openai.api_key = os.environ.get("OPENAI_API_KEY")
#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


try:

    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)
except:
    from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader

    documents = SimpleDirectoryReader("/Users/nehanthnarendrula/Documents/Documents/Projects/ChatUTD/data").load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    index.storage_context.persist()


@cl.llama_index_factory
def factory():
    llm_predictor = LLMPredictor(
        llm=ChatOpenAI(
            temperature=0,
            model_name="gpt-3.5-turbo",
            streaming=True,
        ),
    )
    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor,
        chunk_size=512,
        callback_manager=CallbackManager([cl.LlamaIndexCallbackHandler()]),
    )
    query_engine = index.as_query_engine(
        service_context=service_context,
        streaming=True,
    )

    return query_engine
