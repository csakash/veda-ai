import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai, os, datetime
from llama_index import SimpleDirectoryReader

print("Time to Start the Streamlit App: ", datetime.datetime.now())
st.set_page_config(page_title="Chat with me", page_icon="💬", layout="centered", initial_sidebar_state="auto", menu_items=None)

openai.api_key = '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'

st.title("Chat with Ankur Warikoo")
st.info("Check out my Youtube Channel")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hey, what do you wanna talk about?"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing Ankur's mind"):
        print("Starting to load from the data directory: ", datetime.datetime.now())
        reader = SimpleDirectoryReader(input_dir='./subs', recursive=True)
        docs = reader.load_data()
        print("Data loaded successfully at: ", datetime.datetime.now())

        print("Start indexing at: ", datetime.datetime.now())
        service_context = ServiceContext.from_defaults(
            llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are Ankur Warikoo, an expert of startups, productivity, lifestyle, finance, time management etc. Your job is to personify Ankur Warikoo and answer all the questions calmly and gently"))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)

        print("Indexing completed successfully at: ", datetime.datetime.now())
        return index
    
index = load_data()

print("Starting to load Index into the chat engine at : ")
chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
print("Chat engine loading completed at: ", datetime.datetime.now())

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖"):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking . . ."):
            print("Starting to process the prompt: ", datetime.datetime.now())
            response = chat_engine.chat(prompt)
            print("Prompt generated at: ", datetime.datetime.now())
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)


        