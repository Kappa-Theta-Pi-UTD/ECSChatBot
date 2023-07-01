from flask import Flask, request, jsonify
from llama_index import GPTSimpleVectorIndex, Document, SimpleDirectoryReader
from llama_index.node_parser import SimpleNodeParser
import os
import traceback
import config
import openai

app = Flask(__name__)

# Set the OpenAI API key
openaikey = os.environ.get('OPENAI_API_KEY')

def load_data():
    parser = SimpleNodeParser()
    documents = SimpleDirectoryReader('ecs').load_data()
    documents = parser.get_nodes_from_documents(documents)
    return documents

def load_or_create_index(index_path="index2.json"):
    try:
        if os.path.exists(index_path):
            index = GPTSimpleVectorIndex.load_from_disk(index_path)
        else:
            documents = load_data()
            index = GPTSimpleVectorIndex(documents)
            index.save_to_disk(index_path)
        return index
    except Exception as e:
        print(f"Error during index loading or creation: {str(e)}")
        traceback.print_exc()
        return None



@app.route('/query', methods=['POST'])
def query():
    try:
        index = load_or_create_index()
        data = request.get_json()
        question = data.get('question')

        if question is None:
            return jsonify({'error': 'Invalid request. "question" parameter is missing.'}), 400

        response = index.query(question)
        response = str(response)

        return jsonify({'response': response[1:]})

    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run()
