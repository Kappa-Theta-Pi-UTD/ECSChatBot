from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, LLMPredictor, PromptHelper, ServiceContext
from langchain.chat_models import ChatOpenAI
import openai
import os

os.environ['OPENAI_API_KEY']  = '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'
openai.api_key = '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'
def build_storage(data_dir, persist_dir):
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"))
    max_input_size = 8000
    num_output = 2000
    max_chunk_overlap = 0

    prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)
    documents = SimpleDirectoryReader(r'C:\Users\hamza\OneDrive\Documents\ZN2\ChatBot\ECSChatBot\server\data').load_data()
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
    index.storage_context.persist(persist_dir)

    return index

if __name__ == "__main__":  

    data_dir = "./data"
    persist_dir = "./storage"

    print('Training and building new storage...')
    build_storage(data_dir, persist_dir)
    print('Done!')
