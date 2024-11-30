# Install required packages using the terminal if not already installed:
# pip install streamlit langchain openai

import streamlit as st
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Global CSS for styling
st.markdown(
    """
    <style>
    html, body, .block-container {
        font-size: 1rem;
    }
    .title {
        font-size: 2rem !important;
        font-weight: bold;
        color: green;
        text-align: center;
        margin-bottom: 5px
    }
    input {
        font-size: 2rem;
        padding: 15px;
        border: 2px solid #d1d1d1;
        border-radius: 8px;
        width: 100%;
    }
    ::placeholder {
        font-size: 1rem;
        color: #a1a1a1;
    }
    .textbox {
        font-size: 1rem;
        padding: 15px;
        border: 1px solid #d1d1d1;
        border-radius: 8px;
        margin-top: 10px;
        background-color: #f9f9f9;
    }
    div.stButton > button:first-child {
        background-color: lightgrey;
        color: black;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 8px;
        border: 2px solid grey;
    }
    div.stButton > button:first-child:hover {
        background-color: darkgrey;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.markdown('<div class="title">Scottish Gaelic Phrase Generator</div>', unsafe_allow_html=True)

# Input Section
st.markdown('<label for="topic" style="font-size: 1.2rem; margin-bottom: 2px;">Enter a topic:</label>', unsafe_allow_html=True)
topic = st.text_input("", key="topic", placeholder="Type your topic here...", label_visibility="collapsed")

# Initialize session state
if "generated_phrase" not in st.session_state:
    st.session_state["generated_phrase"] = ""
if "english_translation" not in st.session_state:
    st.session_state["english_translation"] = ""
if "example_sentence" not in st.session_state:
    st.session_state["example_sentence"] = ""

# Initialize the chat model
model = ChatOpenAI(model="gpt-4o", openai_api_key=openai_api_key)

# Columns for layout
col1, col2, col3 = st.columns(3)

# Generate Gaelic Phrase
with col1:
    if st.button("Generate Gaelic Phrase"):
        if not topic.strip():
            st.error("Please enter a topic.")
        else:
            try:
                prompt_template = ChatPromptTemplate([
                    ("system", "You are a helpful Scottish Gaelic assistant for 10-year-old students."),
                    ("user", "Give me a very simple Scottish Gaelic phrase about this {topic} with phonetic pronunciation. I only want the Scottish Gaelic and the pronunciation. Do not translate this into English.")
                ])
                chain = prompt_template | model
                response = chain.invoke({'topic': topic})
                st.session_state["generated_phrase"] = response.content
            except Exception as e:
                st.error(f"An error occurred: {e}")

if st.session_state["generated_phrase"]:
    st.markdown(
        f"""
        <div class="textbox">
            <b>Generated Gaelic Phrase:</b>
            <p>{st.session_state["generated_phrase"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Translate to English
with col2:
    if st.button("Translate to English"):
        if not st.session_state.get("generated_phrase"):
            st.error("Please generate a Gaelic phrase first.")
        else:
            try:
                translation_prompt = ChatPromptTemplate([
                    ("system", "You are a helpful Scottish Gaelic assistant for 10-year-old students."),
                    ("user", "Translate this {phrase} into English.")
                ])
                chain = translation_prompt | model
                translation_response = chain.invoke({'phrase': st.session_state["generated_phrase"]})
                st.session_state["english_translation"] = translation_response.content
            except Exception as e:
                st.error(f"An error occurred: {e}")

if st.session_state["english_translation"]:
    st.markdown(
        f"""
        <div class="textbox">
            <b>English Translation:</b>
            <p>{st.session_state["english_translation"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Use it in a Sentence
with col3:
    if st.button("Use it in a Sentence"):
        if not st.session_state.get("generated_phrase"):
            st.error("Please generate a Gaelic phrase first.")
        else:
            try:
                sentence_prompt = ChatPromptTemplate([
                    ("system", "You are a helpful Scottish Gaelic assistant for 10-year-old students."),
                    ("user", "Use this Scottish Gaelic phrase in a sentence: {phrase}. Provide the English translation.")
                ])
                chain = sentence_prompt | model
                sentence_response = chain.invoke({'phrase': st.session_state["generated_phrase"]})
                st.session_state["example_sentence"] = sentence_response.content
            except Exception as e:
                st.error(f"An error occurred: {e}")

if st.session_state["example_sentence"]:
    st.markdown(
        f"""
        <div class="textbox">
            <b>Example Sentence:</b>
            <p>{st.session_state["example_sentence"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
