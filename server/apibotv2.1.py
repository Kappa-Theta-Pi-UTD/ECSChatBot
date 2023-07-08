from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, LLMPredictor, PromptHelper, ServiceContext
from llama_index import load_index_from_storage, StorageContext
from llama_index.storage.storage_context import StorageContext
from llama_index.node_parser import SimpleNodeParser
from langchain import OpenAI
import os
import traceback
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS



app = Flask(__name__)
CORS(app) 


if not os.environ.get('OPENAI_API_KEY'):
    os.environ['OPENAI_API_KEY']  = 'your-api-key-here'


def build_storage(data_dir):
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003"))

    max_input_size = 8000

    num_output = 2000

    max_chunk_overlap = 0

    prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

    documents = SimpleDirectoryReader('ecs').load_data()

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
    # service_context==service_context
    index.storage_context.persist()

    return index

def read_from_storage(persist_dir):
    print("here12")
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    return load_index_from_storage(storage_context)


@app.route('/query', methods=['POST'])
def query():
    persist_dir = "./storage"
    data_dir = "./data"
    index = None
    print('here2')
    if os.path.exists(persist_dir):
        index = read_from_storage(persist_dir)
    else:
        index = build_storage(data_dir)
        

    data = request.get_json()
    question = data.get('question')
    query_engine = index.as_query_engine()
    response  = query_engine.query(question)
    response = str(response)

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run()

