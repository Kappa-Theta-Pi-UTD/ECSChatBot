from llama_index import LLMPredictor, SimpleDirectoryReader, ServiceContext, LangchainEmbedding, GPTVectorStoreIndex, StorageContext
from llama_index. readers. chroma import ChromaReader 
from llama_index.vector_stores import ChromaVectorStore 
from langchain.chat_models import ChatOpenAI
from llama_index.prompts.prompts import QuestionAnswerPrompt 
from llama_index. logger import LlamaLogger 
from langchain.embeddings import HuggingFaceEmbeddings 
from llama_index.indices.prompt_helper import PromptHelper
from langchain import HuggingFaceHub
from huggingface_hub import hf_hub_download
from dotenv import load_dotenv
from llama_index.node_parser import SimpleNodeParser
from sentence_transformers import SentenceTransformer
import os
import requests

load_dotenv()


import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings

llama_logger = LlamaLogger()

chroma_dir = "database"
chroma_client = chromadb.Client(Settings(
    chroma_db_impl ='duckdb+parquet',
    persist_directory=chroma_dir,
    anonymized_telemetry=False
))
index_name= "ecs"

print('here1')

# model_id = "sentence-transformers/all-MiniLM-L6-v2"
# hf_token = "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"

# api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
# headers = {"Authorization": f"Bearer {hf_token}"}

# model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# model = HuggingFaceHub(repo_id="google/flan-t5-large",
#                        model_kwargs={"temperature": 0, "max_length":200},
#                        huggingfacehub_api_token=  os.getenv( "HUGGINGFACEHUB_API_TOKEN" ))
model = HuggingFaceHub(repo_id="facebook/mbart-large-50",
                       model_kwargs={"temperature": 0, "max_length":200},
                       huggingfacehub_api_token= os.getenv( "HUGGINGFACEHUB_API_TOKEN" ))

print('here2')


# tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
# model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
chroma_collection_name = index_name
chroma_collection = chroma_client.get_or_create_collection(chroma_collection_name,
embedding_function=sentence_transformer_ef)
embed_model = embedding_functions.DefaultEmbeddingFunction()

print('here3')


max_input_size = 3000

num_output = 256

max_chunk_overlap = 1
prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=1000))
print('here4')

service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, llama_logger=llama_logger, prompt_helper=prompt_helper)
vector_store = ChromaVectorStore(embed_model=embed_model, chroma_collection=chroma_collection,service_context=service_context)
print('here5')

# parser = SimpleNodeParser()how
documents = SimpleDirectoryReader('ecs').load_data()
# documents = parser.get_nodes_from_documents(documents)

storage_context = StorageContext.from_defaults(vector_store=ChromaVectorStore(chroma_collection=chroma_collection))
print('here6')


index = GPTVectorStoreIndex.from_documents(documents, storage_context=storage_context, service_context=service_context)

index.storage_context.persist()

query_engine = index.as_query_engine(similarity_top_k=1)
# print('here7')

response = query_engine.query("How long until I graduate?")
print('here8')

print(llm_predictor.last_token_usage)
print('here9')

print(response)