from langchain import PromptTemplate, HuggingFaceHub, LLMChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from huggingface_hub import hf_hub_download
import os
import textwrap
import glob

template = """ You are going to be my assistant.
Please try to give me the most beneficial answers to my
question with reasoning for why they are correct.

 Question: {input} Answer: """
prompt = PromptTemplate(template=template, input_variables=["input"])

model = HuggingFaceHub(repo_id="facebook/mbart-large-50",
                       model_kwargs={"temperature": 0, "max_length":200},
                       huggingfacehub_api_token= os.getenv( "HUGGINGFACEHUB_API_TOKEN" ))
chain = LLMChain(prompt=prompt, llm=model)

hf_embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

my_loader = DirectoryLoader('ecs', glob='**/*.pdf')
docs = my_loader.load()
text_split = RecursiveCharacterTextSplitter(chunk_size = 700, chunk_overlap = 0)
text = text_split.split_documents(docs)

vectorstore = FAISS.from_documents(text, hf_embeddings)

my_chain = load_qa_with_sources_chain(model, chain_type="refine")
query = "What is ECS?"
documents = vectorstore.similarity_search(query)
result = my_chain({"input_documents": documents, "question": query})
print(result)
