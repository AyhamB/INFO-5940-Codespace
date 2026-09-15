# Streamlit builds the page; OpenAI provides the client for model API calls.
import streamlit as st
from openai import OpenAI

# Use the API key and Cornell gateway address from our environment.
# Creating the client prepares the connection; the model call happens below.
client = OpenAI()
st.title("Our Chatbot")

# After editing this instruction, click New conversation to use it.
system_prompt = "You are a helpful tutor. Explain your answers clearly."
# This returns True on the run triggered by clicking the button.
new_conversation = st.button("New conversation")

# Streamlit reruns this file after each submission or button click.
# Session state keeps our messages between runs. Initialize it or start over.
if "messages" not in st.session_state or new_conversation:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

# Redraw earlier messages. Keep the system instruction out of the visible chat.
for message in st.session_state.messages:
    if message["role"] != "system":
        # The indented display call goes inside a chat container for this role.
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Returns submitted text, or None when no message was submitted on this run.
question = st.chat_input("Ask a question")

# Only call the model when the user submits a new message.
if question:
    # Make a new list containing the saved conversation and the new question.
    # Using + leaves the saved history unchanged until we have an answer.
    request_messages = st.session_state.messages + [
        {"role": "user", "content": question}
    ]
    # Show the new question now; the earlier loop only displayed saved messages.
    with st.chat_message("user"):
        st.markdown(question)

    # OPTION 1: Wait for the complete answer (enabled by default).
    # Send the entire conversation, then extract the first assistant reply.
    response = client.chat.completions.create(
        model="openai.gpt-4o",
        messages=request_messages,
    )
    # choices[0] selects the first choice; message.content holds its text.
    answer = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.markdown(answer)

    # OPTION 2: Stream the answer as it arrives.
    # To enable: comment out Option 1's code above, then uncomment these 7 lines.
    # Keep only one option active so each question makes one API call.
    # stream = client.chat.completions.create(
    #     model="openai.gpt-4o",
    #     messages=request_messages,
    #     stream=True,
    # )
    # with st.chat_message("assistant"):
    #     answer = st.write_stream(stream)

    # write_stream displays the pieces and returns the complete answer text.
    # Both options use `answer`, so the history update below works with either.

    # Save both sides of this exchange so the next request can include them.
    st.session_state.messages = request_messages + [
        {"role": "assistant", "content": answer}
    ]
