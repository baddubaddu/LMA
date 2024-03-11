import time
from dotenv import load_dotenv
import streamlit as st
from app_style import css, bot_template, user_template
from llm_chain import RAG_PDF

logo_image_path = "logo2.png"

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    # loading environment varibales
    load_dotenv()
    # Page Config
    st.set_page_config(page_title="Let Me Answer",
                       page_icon=":rocket:")
    st.write(css, unsafe_allow_html=True)
    # Chat history session management

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    
    # for rendering the background image (Uncomment the next line to update the background img of the application)
    # render_background_img(background_path)
    
    # Chat User input
    st.header(":green[Let Me Answer]:rocket:")
    user_question = st.text_input("**:green[Ask me anything about your document]**")
    styl = f"""
            <style>
                .stTextInput {{
                position: fixed;
                bottom: 3rem;
                }}
            </style>
            """
    st.markdown(styl, unsafe_allow_html=True)


    # Handling user input
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        # Loading the Logo
        st.image(logo_image_path, use_column_width=True)
        
        # Header text for the sidebar
        st.subheader(":green[Your documents]")

        # File Uploader (Allowing multiple files upload)
        pdf_docs = st.file_uploader(
            "**:green[Upload your PDFs here and click on 'Read']**", accept_multiple_files=True)
        
        # When the submit button is clicked
        if st.button("**:green[Read]**"):
            # Processing
            with st.spinner("**:rainbow[Reading]**"):
                RAG_object = RAG_PDF(pdf_docs)
                # Activating the RAG Pipeline
                st.session_state.conversation = RAG_object.activate_RAG_pipeline()
                # Posting an update when the upload and processing of RAG architecture done
                st.write("**:green[Reading Completed.]**")
                st.balloons()

if __name__ == '__main__':
    main()