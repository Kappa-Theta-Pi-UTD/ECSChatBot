import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
# from llama_index import GPTSimpleVectorIndex, Document, SimpleDirectoryReader
# from llama_index.node_parser import SimpleNodeParser
# import os
# import openai

from llama_index import VectorStoreIndex, Document, SimpleDirectoryReader
from llama_index import StorageContext, load_index_from_storage
from llama_index.node_parser import SimpleNodeParser
import openai
import os

# Set the OpenAI API key

title = '<p style="font-family: Georgia; color:white; text-align: center; font-size: 50px;">ECS ChatBot</p>'
st.markdown(title, unsafe_allow_html=True)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("----")

openaikey = st.text_input("Enter your openAI key: ")
openai.api_key = openaikey


def load_data():
    parser = SimpleNodeParser()
    documents = SimpleDirectoryReader('ecs').load_data()
    documents = parser.get_nodes_from_documents(documents)
    return documents


def load_or_create_index(index_path="index3.json"):
    try:
        if "index" not in st.session_state:
            if os.path.exists(index_path):
                # st.session_state.index = GPTSimpleVectorIndex.load_from_disk(index_path)
                storage_context = StorageContext.from_defaults(
                    persist_dir=index_path)
                st.session_state.index = load_index_from_storage(
                    storage_context)
            else:
                documents = load_data()
                # st.session_state.index = GPTSimpleVectorIndex(documents)
                # st.session_state.index.save_to_disk(index_path)
                st.session_state.index = VectorStoreIndex(documents)
                st.session_state.index.storage_context.persist(
                    persist_dir="index3.json")
        return st.session_state.index
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


index = load_or_create_index()

# if index is not None:
#     question = st.text_input("Enter your question: ")
#     st.markdown("----")
#     # response = index.query(question)
#     # response = str(response)
#     # st.write(str(response[1:]))
#     query_engine = index.as_query_engine()
#     response = query_engine.query(question)
#     st.write(response.response)

#     st.markdown("----")
# else:
#     st.warning("Index could not be loaded or created.")


question = st.text_input("Enter your question: ")
st.markdown("----")
# response = index.query(question)
# response = str(response)
# st.write(str(response[1:]))

query_engine = index.as_query_engine()
response = query_engine.query(question)
st.write(response.response)

st.markdown("----")

title2 = '<p style="font-family: Georgia; color:white; text-align: center; font-size: 35px;">Powered by</p>'
st.markdown(title2, unsafe_allow_html=True)

img = Image.open("ktplogo.png")
col1, col2, col3 = st.columns([0.2, 0.2, 0.2])
col2.image(img, use_column_width=True)
