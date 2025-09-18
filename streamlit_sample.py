import streamlit as st

st.set_page_config(page_title="Hello Codespaces", layout="centered")

st.title("👋 Hello from Codespaces!")
st.write("If you can see this page, Streamlit is running correctly inside your Codespace.")

name = st.text_input("What is your name?")
if name:
    st.success(f"Nice to meet you, {name}!")

st.markdown("---")
st.caption("This is a test app for INFO 5940 Fall 2025.")