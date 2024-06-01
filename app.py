import streamlit as st
from RAG import generate_answer

st.title("RAG Model Benefit Demonstration")
st.header("\n A Simplified Approach")

if 'selection' not in st.session_state:
    st.session_state.selection = ""

Options = False
emp = st.empty()
vari = emp.selectbox(
    key = "Options",
    label = "Please select the option for query running:",
    options = ("Wikipedia", "Research Paper")
)

if st.button("Select"):
    choice = vari
    Options = True


def wiki_choice() -> str:
    wiki_query = st.text_input(
        label = "Please input your Wikipedia search query",
        max_chars = 256
    )

    if st.button("Submit"):
        return wiki_query


def research_choice() -> str:
    research_query = st.text_input(
        label = "Please input your document search query",
        max_chars = 256
    )

    if st.button("Submit"):
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
    if Options:
        st.session_state.selection = choice

    main(st.session_state.selection)
