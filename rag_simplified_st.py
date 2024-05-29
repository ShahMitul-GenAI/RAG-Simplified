import streamlit as st
from subprocess import call
from pathlib import Path
import os.path
import time
import pickle
import json
from RAG_Simplified import generate_answer

# import warnings
# warnings.filterwarnings("ignore")

check_notifications = "C:/Users/Mast_Nijanand/RAG Simplified/notifications/"

st.title("RAG Model Benefit Demonstration")

if 'selection' not in st.session_state:
    st.session_state.selection = ""

Options = False
emp = st.empty()
vari = emp.selectbox(key = "Options",
                            label = "Please select the option for query running:",
                            options = ("Wikipedia", "Research Paper", "Both"))
if st.button("Select"):
    choice = vari
    Options = True

# clearing previously loaded pool of notification files
target_folder = str(os.path.dirname(os.path.abspath(__file__))) + "/notifications/"
delete_files = [f.unlink() for f in Path(str(target_folder)).iterdir() if f.is_file()]
del delete_files

# function to execute backend python file
def run_file():
    call(["python", "RAG_Simplified.py"])

def wiki_choice() -> str:
    wiki_query = st.text_input(
        label = "Please input your Wikipedia search query",
        max_chars = 256)
    if st.button("Submit"):
        return wiki_query

def research_choice() -> str:
    research_query = st.text_input(
        label = "Please input your document search query",
        max_chars = 256)
    if st.button("Submit"):
        return research_query

def combined_choice():
    combined_query1 = st.text_input(
        label="Please input your query for Wikipedia search",
        max_chars=256)

    combined_query2 = st.text_input(
        label="Please input your query for Research Paper search",
        max_chars=256)
    if st.button("Submit"):
        return combined_query1, combined_query2

# TODO: add spinner to main function instead of here
def routine_process(answer: str):
    # with st.spinner("Processing your request..."):
    #     # display = []
    #     assert os.path.exists("C:/Users/Mast_Nijanand/RAG Simplified/notifications/wiki_out.json")
    st.success("Data processing complete!")
    # with open("C:/Users/Mast_Nijanand/RAG Simplified/notifications/wiki_out.json", 'r') as fp:
    st.markdown(f"### {answer['result']}")

def dual_process(notify1, notify2):
    while st.spinner("Processing your request..."):
        display1 = []
        display2 = []
        while not os.path.exists(str(check_notifications) + "PROG EXIT.txt"):
            time.sleep(1)
            for i in range(2):
                if i == 0:
                    if os.path.exist(str(check_notifications) + str(i + 1) + str("txt")):
                        with open((str(check_notifications) + str(notify1)), 'r') as fp:
                            lines = fp.read()
                            line = lines.splitlines()
                        for each in line:
                            display1.append(each)
                else:
                    if os.path.exist(str(check_notifications) + str(i + 1) + str("txt")):
                        with open((str(check_notifications) + str(notify2)), 'r') as fp:
                            lines = fp.read()
                            line = lines.splitlines()
                        for each in line:
                            display2.append(each)
                        break
        st.markdown("## Output from the Wikipedia search")
        for each in display1:
            st.write(each)

        st.markdown("## Output from the Research Paper search")
        for each in display2:
            st.write(each)
    st.success("Data processing complete!")

def main(selection):
    if selection == "Wikipedia":
        wiki_query = wiki_choice()

        if wiki_query is not None:
            # storing query output for further processing
            with open("./notifications/wiki_query.txt", "w") as fp:
                fp.write(str(wiki_query))
            pickle.dumps("wiki_query.txt")

            answer = generate_answer(selection)
            routine_process(answer)
    elif selection == "Research Paper":
        research_query = research_choice()

        if research_query is not None:
            # storing query for further processing & exporting
            with open("./notifications/doc_query.txt", "w") as fp:
                fp.write(str(research_query))
            pickle.dumps("doc_query.txt")

            answer = generate_answer(selection)
            routine_process(answer)

if __name__ == "__main__":
    if Options:
        st.session_state.selection = choice

    # writing option selection in an output file
    with open("./notifications/option.txt", "w") as fopt:
        fopt.write(str(st.session_state.selection))
    pickle.dumps("option.txt")

    # calling main function
    main(st.session_state.selection)
