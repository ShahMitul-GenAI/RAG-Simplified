import os, os.path
import shutil
import pathlib
import streamlit as st
from simplified_rag.RAG import generate_answer

st.title("RAG Model Benefit Demonstration")
st.header("\n A Simplified Approach")

if 'selection' not in st.session_state:
    st.session_state.selection = ""

# clearing previously loaded pool of docs
target_folder = pathlib.Path().absolute()  / "docs/"

if target_folder.exists():
    shutil.rmtree(target_folder)
target_folder.mkdir(parents=True, exist_ok=True)

# activating selection box for user choice 
options = False
emp = st.empty()
vari = emp.selectbox(
    key = "Options",
    label = "Please select the option for query running:",
    options = ("Wikipedia", "Research Paper")
)

if st.button("Select"):
    choice = vari
    options = True


def wiki_choice() -> str:
    wiki_query = st.text_input(
        label = "Please input your Wikipedia search query",
        max_chars = 256
    )

    if st.button("Submit"):
        return wiki_query


def research_choice() -> str:
    
    with st.form(key="doc_upload", clear_on_submit=False):

        uploaded_doc = st.file_uploader(
            label="Please upload your document",
            accept_multiple_files = False,
            type=['pdf']
        )
        research_query = st.text_input(
            label = "Please input what you want to search",
            max_chars = 256
        )
        submit_button1 = st.form_submit_button("Load Document")

    if submit_button1:
        with open(os.path.join(target_folder, uploaded_doc.name), 'wb') as f:
            f.write(uploaded_doc.getbuffer())
        return research_query


def main(selection):
    if selection == "Wikipedia":
        wiki_query = wiki_choice()

        if wiki_query is not None:
            with st.spinner("Processing your request..."):
                answer = generate_answer(selection, wiki_query)

                st.success("Data processing complete!")
                st.markdown(f"###### {answer['result']}")
    elif selection == "Research Paper":
        research_query = research_choice()

        if research_query is not None:
            with st.spinner("Processing your request..."):
                answer = generate_answer(selection, research_query)

                st.success("Data processing complete!")
                st.write(answer['result'])

if __name__ == "__main__":
    if options:
        st.session_state.selection = choice

    main(st.session_state.selection)
