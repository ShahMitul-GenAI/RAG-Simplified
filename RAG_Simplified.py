import time
import json
import os.path
import pickle
import streamlit as st
from dotenv import load_dotenv
from langchain.agents import Tool
from langchain.chains import RetrievalQA
from langchain.schema.document import Document
from langchain.agents.agent_types import AgentType
from langchain_community.tools import WikipediaQueryRun
from langchain.agents.initialize import initialize_agent
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.utilities import WikipediaAPIWrapper 
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_community.vectorstores import DocArrayInMemorySearch
from typing import Any, Literal, get_args

DataSource = Literal["Wikipedia", "Research Paper"]
SUPPORTED_DATA_SOURCES = get_args(DataSource)

# loading API keys from env
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# loading model and defining embedding
llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')
embeddings = OpenAIEmbeddings()

def get_query(source: DataSource) -> str:
    if source not in SUPPORTED_DATA_SOURCES:
        raise ValueError(f"Provided data source {source} is not supported.")

    if source == "Wikipedia":
        filename = "wiki_query.txt"
    else:
        filename = "doc_query.txt"

    assert os.path.exists(f"./notifications/{filename}")

    with open(f"./notifications/{filename}", 'r') as f:
        query = f.read()
    
    return query

def load_data_set(source: DataSource, query: str):
    if source not in SUPPORTED_DATA_SOURCES:
        raise ValueError(f"Provided data source {source} is not supported.")

    if source == "Wikipedia":
        Wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        data = Wikipedia.run(query)
    else:
        loader = PyPDFLoader("./2312.10997v5.pdf")
        data = loader.load()

    # fragmegting the document content to fit in the number of token limitations
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)

    if source == "Wikipedia":
        split_docs = [Document(page_content=sent) for sent in data.split('\n')]
    else:
        split_docs = text_splitter.split_documents(data)

    data_set = DocArrayInMemorySearch.from_documents(documents = split_docs, embedding = embeddings)
    print(type(data_set))

    return data_set


def retrieve_info(source: DataSource, data_set: Any, query: str):
    if source not in SUPPORTED_DATA_SOURCES:
        raise ValueError(f"Provided data source {source} is not supported.")

    qa = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type="stuff",
        retriever = data_set.as_retriever(), # repla
        verbose=True,
    )

    output = qa.invoke(query)

    return output

# determining prompts as per search selection option 
def generate_answer(selection: DataSource):
    if selection not in SUPPORTED_DATA_SOURCES:
        raise ValueError(f"Provided data source {selection} is not supported.")

    if selection == "Wikipedia":
        while not os.path.exists("./notifications/wiki_query.txt"):
            time.sleep(5)

        query = get_query(selection)
        data_set = load_data_set(selection, query)
        response = retrieve_info("Wikipedia", data_set, query)
    elif selection == "Research Paper":
        while not os.path.exists("./notifications/doc_query.txt"):
            time.sleep(5)

        query = get_query(selection)
        data_set = load_data_set(selection, query)
        response = retrieve_info("Research Paper", data_set, query)
    
    return response