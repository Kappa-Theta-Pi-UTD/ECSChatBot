from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, LLMPredictor, PromptHelper, ServiceContext
from llama_index import load_index_from_storage, StorageContext
from llama_index.storage.storage_context import StorageContext
from llama_index.node_parser import SimpleNodeParser
from langchain import OpenAI
import os
import traceback
from flask import Flask, request, jsonify



app = Flask(__name__)




if not os.environ.get('OPENAI_API_KEY'):
    os.environ['OPENAI_API_KEY']  = 'your-api-key-here'

def load_or_create_index():

    documents = SimpleDirectoryReader('ecs').load_data()

    try:
        # storage_context = StorageContext.from_defaults(persist_dir="./storage")
        index = GPTVectorStoreIndex.load_from_disk('index.json')
    except:

        # index  = GPTVectorStoreIndex([])

        # index = GPTVectorStoreIndex.from_documents(documents)

        llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.1, model_name="text-davinci-003"))

        max_input_size = 4096

        num_output = 512

        max_chunk_overlap = 1

        prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

        index = GPTVectorStoreIndex.from_documents(documents, service_context==service_context)

        # for doc in documents:
        #     index.insert(doc)

        index.save_to_disk('index.json')

        # index.storage_context.persist()

    return index




@app.route('/query', methods=['POST'])
def query():
    try:
        index = load_or_create_index()
        data = request.get_json()

        question = data.get('question')

        if question is None:
            return jsonify({'error': 'Invalid request. "question" parameter is missing.'}), 400


        query_engine = index.as_query_engine()
        response  = query_engine.query(question)
        response = str(response)

        return jsonify({'response': response[1:]})

    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run()

