from dotenv import load_dotenv
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, LLMPredictor, PromptHelper, ServiceContext
from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
import os

app = Flask(__name__)

def get_pdf_text(pdf_docs):
    text = ""
    print(pdf_docs)
    for pdf in pdf_docs:
        print(pdf)
        with open(pdf,"rb") as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    return text

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks

# OpenAI embeddings
def get_vectorstore_Open(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts = text_chunks, embedding=embeddings)
    return vectorstore

def get_vectorstore_Hugging(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts = text_chunks, embedding=embeddings)
    return vectorstore



def main():
    load_dotenv()

    # pdf_docs = open('ecsadvising2.pdf', "rb")
    pdf_file = []
    for filename in os.listdir('./ecs'):
            #print(filename)
            pdf_file = open(os.path.join('./ecs', filename), 'rb')
            print(pdf_file)

    # pdf_docs = SimpleDirectoryReader('ecs').load_data()
    raw_text = get_pdf_text(pdf_file)

    text_chunks = get_text_chunks(raw_text)

    vectorstore = get_vectorstore_Hugging(text_chunks)

    #______________________UNDER DEVELOPMENT_________________________#


if __name__ == '__main__':
   main()