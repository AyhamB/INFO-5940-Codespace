# import streamlit as st

# st.set_page_config(page_title="Hello Codespaces", layout="centered")

# st.title("👋 Hello from Codespaces!")
# st.write("If you can see this page, Streamlit is running correctly inside your Codespace.")

# name = st.text_input("What is your name?")
# if name:
#     st.success(f"Nice to meet you, {name}!")

# st.markdown("---")
# st.caption("This is a test app for INFO 5940 Fall 2025.")


import streamlit as st
import os
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


st.set_page_config(page_title="Hello Codespaces", layout="centered")


st.title("👋 Hello from Codespaces!")
st.write("If you can see this page, Streamlit is running correctly inside your Codespace.")


name = st.text_input("What is your name?")
if name:
   st.success(f"Nice to meet you, {name}!")


st.markdown("---")
st.caption("This is a test app for INFO 5940 Fall 2025.")


with open("data/knowledge_base.txt") as f:
   knowledge_base = f.read()



if "messages" not in st.session_state:
   st.session_state["messages"] = [
      {"role": "assistant", "content": "Howdy!"},
      {"role": "system", "content": (
            "You are a helpful assistant that helps people find information. "
            "Use the following knowledge base to answer questions:\n\n"
            f"{knowledge_base}"
         ),},
      {"role": "user", "content": "I want you to answer questions based on this knowledge database"},
                                   ]


for msg in st.session_state.messages:
   if msg['role'] != 'system':
       st.chat_message(msg['role']).write(msg['content'])


if prompt := st.chat_input():
   st.session_state.messages.append({"role": "user", "content": prompt})
   st.chat_message("user").write(prompt)


   with st.chat_message("assistant"):
       stream = client.chat.completions.create(model = "openai.gpt-4o", messages = st.session_state.messages, stream = True)
       response = st.write_stream(stream)


   st.session_state.messages.append({"role": "assistant", "content": response})



