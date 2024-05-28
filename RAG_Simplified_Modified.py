# %%
import time
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

# %%
# loading API keys from env
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# %%
# loading model and defining embedding
llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')
embeddings = OpenAIEmbeddings()

# %%
# importing inputs from UI 
fslk = open("./notifications/option.txt", "r")
selection = fslk.read()
fslk.close()

# determining prompts as per search selection option 
if selection == "Wikipedia":
    while not os.path.exists("./notifications/wiki_query.txt"):
        time.sleep(5)
    if os.path.exists("./notifications/wiki_query.txt"):
        f1 = open("./notifications/wiki_query.txt", 'r')
        query = f1.read()
        f1.close()
        print(f"wiki prompt after selection is {query}")
elif selection == "Research Paper":
    while not os.path.exists("./notifications/doc_query.txt"):
        time.sleep(5)
    if os.path.exists("./notifications/doc_query.txt"):
        f2 = open("./notifications/doc_query.txt", 'r')
        query = f2.read()
        f2.close()
        print(f"Docu prompt after selection is {query}")
else:
    while not os.path.exists("./notifications/cmd_qr2.txt.txt"):
        time.sleep(5)
    if os.path("./notifications/cmd_qr2.txt"):
        f3 = open("./notifications/cmd_qr1.txt", 'r')
        query1 = f3.read()
        f4 = open("./notifications/cmd_qr2.txt", 'r')
        query2 = f4.read()
        f3.close()
        f4.close()
        print(f"wiki3 prompt after selection is {query1}")
        print(f"docu3 prompt after selection is {query2}")

# %%
# setting up info retreival from Wikipedia pages (1st knowledge source)
if selection == "Wikipedia":
    print(f"wiki prompt insider wrapper is {query}")
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    wiki_output = wikipedia.run(query)

# %%
# fragmegting the document content to fit in the number of token limitations
if selection == "Wikipedia":
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
    new_docs = [Document(page_content=sent) for sent in wiki_output.split('\n')]

# splitted_output = text_splitter.split_documents(new_doc)
    data_set = DocArrayInMemorySearch.from_documents(new_docs, embedding=embeddings)

# %%
# retreiving the llm response using user query
if selection == "Wikipedia":
    qa = RetrievalQA.from_chain_type(
        llm =llm,
        chain_type="stuff",
        retriever = data_set.as_retriever(),
        verbose=True,
    )

# %%
if selection.strip() == "Wikipedia":
    wiki_out = qa.invoke(query)
    with open("./notifications/wiki_out.txt", 'w') as fwk:
        fwk.write(str(wiki_out)['result'])
        pickle.dumps("wiki_out.txt")

# %%
# Loading research paper from web source (2nd knoledge source)

if selection == "Research Paper":
    loader = PyPDFLoader("./2312.10997v5.pdf")
    docs = loader.load()

# fragmegting the document content to fit in the number of token limitations
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
    splits = text_splitter.split_documents(docs)

# load the 
    data_set = DocArrayInMemorySearch.from_documents(documents=splits, embedding=embeddings)

# %%
# retreiving the llm response using user query

if selection == "Research Paper":
    qa = RetrievalQA.from_chain_type(
        llm =llm,
        chain_type="stuff",
        retriever = data_set.as_retriever(),
        verbose=True,
    )

# %%
# get query from U/I now
if selection == "Research Paper":
    result = qa.invoke(query)
    with open("./notifications/doc_out.txt", 'w') as frp:
        frp.write(str(resul['result']))
    pickle.dumps("doc_out.txt")

# %%
# combining two RAG knoledge sources together for better performance

if selection == "Both":
    wiki_tool = Tool(
        name = "wikipedia",
        func = wikipedia.run,
        description = "A useful tool to search internet for the requested information",
    )
    
    docsearch_tool = Tool(
        name = "docsearch",
        func = qa.run,
        description = "A tool to search information from the pool of documents",
    )
    
    agent= initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose = False,
        handle_pasring_errors = True,
    )

# %%
# executing the agent for both knowledgebase options

if selection == "Both":
    result1 = agent.invoke(str(query1))
    result2 = agent.invoke(str(query2))
    
    with open("./notifications/1.txt", 'w') as f1:
        f1.write(str(resul1['output']))
        pickle.dumps("1.txt")
    with open("./notifications/2.txt", 'w') as f2:
        f2.write(str(result2['output']))
        pickle.dumps("2.txt")

# %%
# exporting program ending indicator
ffnl = open("./notifications/PROG EXIT.txt", "rb")
pickle.dumps(123, ffnl)
ffnl.close()


