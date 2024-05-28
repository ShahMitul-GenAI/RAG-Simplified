import streamlit as st
from subprocess import call
from pathlib import Path
import os.path
import time
import pickle
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
    call(["python", "RAG_Simplified_Modified.py"])

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

def routine_process(notify):
    while st.spinner("Processing your request..."):
        display = []
        while not os.path.exists(str(check_notifications) + "PROG EXIT.txt"):
            time.sleep(3)
            if os.path.exist(str(check_notifications) + str(notify)):
                with open((str(check_notifications) + str(notify)), 'r') as fp:
                    lines = fp.read()
                    line = lines.splitlines()
                for each in line:
                    display.append(each)
                break
        for each in display:
            st.write(each)
    st.success("Data processing complete!")

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

def main_func(option):
    print("file ran before")
    run_file()
    print("file ran after")
    if option == "Wikipedia":
        wiki_query = wiki_choice()

        if wiki_query is not None:
            # storing query output for further processing
            with open("./notifications/wiki_query.txt", "w") as fp:
                fp.write(str(wiki_query))
            pickle.dumps("wiki_query.txt")

            # loading run file output
            while not os.path.exists(check_notifications + "wiki_out.txt"):
                time.sleep(1)
                if os.path.exists(check_notifications + "wiki_out.txt"):
                    fwk = open('./notifications/wiki_out.txt', 'r')
                    wiki_out = fwk.read()
                    fwk.close()

            routine_process(notify = wiki_out)

    elif (option == "Research Paper"):
        research_query = research_choice()

        if research_query is not None:
            # storing query for further processing & exporting
            with open("./notifications/doc_query.txt", "w") as fp:
                fp.write(str(research_query))
            pickle.dumps("doc_query.txt")

            # loading run file output
            while not os.path.exists(check_notifications + str("PROG EXIT")):
                time.sleep(1)
                if os.path.exists(check_notifications + str("doc_out.txt")):
                    f2 = open('./notifications/doc_out.txt', 'r')
                    doc_out = f2.read()
                    f2.close()
                    break
            routine_process(notify = doc_out)

    else:
        cb_qr1, cb_qr2 = combined_choice()

        if (cb_qr1 is not None) and (cb_qr2 is not None):
            # storing both queries for further processing & exporting
            fp = open("./notifications/cmd_qr1.txt", "w")
            fp.write(str(cmd_qr1))
            fp.close()
            pickle.dumps("cmd_qr1.txt")

            fq = open("./notifications/cmd_qr2.pkl", "w")
            fq.write(str(cmd_qr2))
            fq.close()
            pickle.dumps("cmd_qr2.txt")

            # loading run file outputs
            while not os.path.exists(check_notifications + str("PROG EXIT")):
                time.sleep(1)
                if os.path.exists(check_notifications + str("2.txt")):
                    fr1 = open('./notifications/1.txt', 'r')
                    one = fr1.read()
                    fr1.close()

                    fr2 = open('./notifications/2.txt', 'r')
                    two = fr1.read()
                    fr2.close()
                    break
            dual_process(notify1 = one, notify2 = two)

# if 'user_inputs' not in st.session_state:
#     st.session_state.user_inputs = []



# function to export user inputs from form
# def export_inputs(data):
#     st.session_state['user_inputs'].append(data)
#     with open("./notifications/data_inputs.pkl", "wb") as fp:
#         pickle.dump(st.session_state.user_inputs, fp)
#
# # displaying page title and header
# st.title("User Inputs for e-Commerce Customer Reviews")
# st.header("Provide the requested information")

# develop form
#
# with st.form(key="user_interaction"):
#     # get new data processing choice
#     new_data_st = st.selectbox(label = "Please select your choice from the dropdown", options = ["Yes", "No"])
#
#     # get name of product in couple to few words
#     product = st.text_input(
#         label = "Please describe your product in 2-5 phrases",
#         max_chars = 30)
#
#     # get number of total customer reviews to process
#     max_cust = st.number_input(
#         label="Select number of Amazon customer reviews to be collected",
#         max_value=50,
#         min_value=10,
#         step=5,
#     )
#     st.session_state.user_inputs = [{"new_data_st": new_data_st, "product": product, "max_cust": max_cust}]
#     submit_button = st.form_submit_button("Submit")
#
# if submit_button:
#     export_inputs(st.session_state.data_collect)
#
#     if new_data_st == "Yes":
#
#         if os.path.exists(str(file_path) + "data_output.pkl"):
#             shutil.move(str(file_path) + "data_output.pkl",
#                         str(file_path) + "review_docs/data_output.pkl")
#         if os.path.exists(str(file_path) + "amazon_reviews_df"):
#             shutil.move(str(file_path) + "amazon_reviews_df",
#                         str(file_path) + "review_docs/amazon_reviews_df")
#
#
#         run_file()
#         new_file_path = str(file_path) + "data_output.pkl"
#         check_notification = str(file_path) + "notifications/"
#
#         with st.spinner("Processing your request....."):
#             while not os.path.exists(str(check_notification) + "PROG EXIT.txt"):
#                 i = 0
#                 j = 0
#                 display = []
#                 while not os.path.exists(str(check_notification) + "PROG EXIT.txt"):
#                     if os.path.exists(str(check_notification) + ("note" + str(i) + ".txt")):
#                         with open((str(check_notification) + ("note" + str(i) + ".txt")), 'r') as fp:
#                             lines = fp.read()
#                             line = lines.splitlines()
#                             for each in line:
#                                 display.append(each)
#                         i += 1
#                     if (os.path.exists(str(check_notification) + 'LARGE.txt')) and (j == 0):
#                         i = 3
#                         j = 1
#                     if os.path.exists(str(check_notification) + ("SMALL.txt")) or (i == 6):
#                         break
#             for each in display:
#                 st.write(each)
#         st.success("Data Processing Complete!")
#         df = pd.DataFrame()
#         df = pd.read_pickle("amazon_reviews_df.pkl")
#         st.write(df)
#     else:
#         st.write("Displaying results of previous product reviews")
#         df = pd.DataFrame()
#         df = pd.read_pickle("amazon_reviews_df.pkl")
#         st.write(df)

if __name__ == "__main__":
    if Options:
        st.session_state.selection = choice

    # writing option selection in an output file
    with open("./notifications/option.txt", "w") as fopt:
        fopt.write(str(st.session_state.selection))
    pickle.dumps("option.txt")

    # calling main function
    main_func(st.session_state.selection)

















