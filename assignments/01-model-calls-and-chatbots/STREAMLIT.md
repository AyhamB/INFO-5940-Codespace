# Build a Conversation with Streamlit

**INFO 5940 · Student activity**

[app.py](app.py) connects a browser chat interface to the same kind of model call
we used in the notebook. This guide explains how the parts fit together, then
gives you three experiments to try. You can run the app independently of the notebook.

For an introduction to Streamlit's widgets and layouts, start with the
[INFO 5940 Streamlit Primer](streamlit-primer/INFO_5940_Streamlit_Primer.md).

## Start the app

In your course Codespace, run this command from the repository root:

```bash
streamlit run assignments/01-model-calls-and-chatbots/app.py
```

Open port **8501** in the **Ports** panel if the browser tab doesn't appear.
Keep the terminal running while you use the app. Press **Ctrl+C** to stop it
before starting another app, such as the primer.

The course environment supplies `OPENAI_API_KEY` and `OPENAI_BASE_URL`.
`OpenAI()` reads these to use your key and Cornell's gateway. If setup is
incomplete, follow the [course README](../../README.md).

## What the app does

- Keeps user and assistant messages during your current session and includes
  them with each new question.
- Starts over when you click **New conversation**. History is temporary;
  the app doesn't save it to a file or database. A browser reload or server
  restart also clears it.
- Displays the complete answer by default. A commented alternative in `app.py`
  enables streaming; Experiment 3 explains how to switch.

## Read the code from top to bottom

Keep `app.py` open alongside this guide. The snippets below are excerpts from
that file, not separate scripts to run.

Streamlit runs the script from top to bottom to build the page. Submitting a
message or clicking a button runs it again. `st.session_state` retains values
between those runs for your session. That is how the app keeps earlier messages.
See the [execution flow](https://docs.streamlit.io/develop/api-reference/execution-flow)
and [session state](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state)
references for more detail.

### 1. Create the client and interface

```python
import streamlit as st
from openai import OpenAI

client = OpenAI()
st.title("Our Chatbot")

system_prompt = "You are a helpful tutor. Explain your answers clearly."
new_conversation = st.button("New conversation")
```

`st` is our short name for the Streamlit module. `OpenAI` is the client class
we import to communicate with the model API. Calling `OpenAI()` creates a
client; it doesn't generate an answer yet.

`st.title` displays the heading. `system_prompt` stores our tutor instruction.
`st.button` displays the reset button and returns `True` on the run triggered
by clicking it. The next block uses that value to reset history.

### 2. Initialize or reset the conversation

```python
if "messages" not in st.session_state or new_conversation:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]
```

`messages` is the name we chose for an entry in session state. We create its
list on the first run, or replace it when the reset button is clicked. Otherwise,
we keep the existing list. Without this condition, every run would replace the
conversation with just the system instruction.

### 3. Display saved messages

```python
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
```

The loop visits each saved message. We skip displaying the system instruction,
but keep it in the list sent to the model. `st.chat_message` creates a container
for a user or assistant message. The indented `st.markdown` call displays the
text inside it, including Markdown formatting such as lists and bold text.

### 4. Read the new question and build its request

```python
question = st.chat_input("Ask a question")

if question:
    request_messages = st.session_state.messages + [
        {"role": "user", "content": question}
    ]
    with st.chat_message("user"):
        st.markdown(question)
```

`st.chat_input` returns submitted text, or `None` if nothing was submitted on
this run. A nonempty question enters the `if` block. Everything below it in the
app runs only for a new submission.

Adding the lists with `+` combines saved history and the new question without
changing the saved list yet. We also display the question because it wasn't in
the history shown by the earlier loop. Displaying a message and sending it to
the model are separate actions.

### 5. Get the model's answer

```python
    response = client.chat.completions.create(
        model="openai.gpt-4o",
        messages=request_messages,
    )
    answer = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.markdown(answer)
```

The call sends the complete message list to GPT-4o through Cornell's gateway.
Python waits for the result. `choices[0]` selects its first choice, `.message`
gets the assistant message, and `.content` gets the answer text for display.

`response` is simply our variable name for the returned Chat Completions object.
The notebook uses `completion` for the same purpose. Neither name changes which
API we call.

### 6. Save both sides of the exchange

```python
    st.session_state.messages = request_messages + [
        {"role": "assistant", "content": answer}
    ]
```

This saves the messages we sent plus the reply we received. On the next turn,
the app can display them and include them in the request. Keeping assistant
replies lets a follow-up such as “Explain your second suggestion” refer to the
actual earlier answer.

If the API call raises an error, execution doesn't reach this assignment, so
the previously saved history remains intact.

### Follow two turns

Starting with a new conversation, here is how the message list grows:

| Action | Messages sent to the API | Saved after the reply |
| --- | --- | --- |
| Open the app | No call | One system message |
| Submit “My name is Bob.” | System instruction + introduction | System, user, assistant |
| Submit “What is my name?” | Three saved messages + new question | System, user, assistant, user, assistant |
| Click **New conversation** | No call | One system message |

The app makes one call for each submitted question. Redrawing saved messages
and updating session state don't make additional API calls.

## Experiment 1: locate the memory

Tell the chatbot “My name is Bob,” then ask “What is my name?” Locate the line
that makes the introduction available to the second request.

Next, ask for three named project ideas and follow up with “Expand the second
idea.” This follow-up depends on the assistant's earlier response. Find the line
that preserves that response.

For an optional view of the stored messages, add this line at the **end of the
file, outside every indented block**:

```python
st.json(st.session_state.messages)
```

This displays the current saved conversation, including the latest assistant
reply. For the exact input to a call, add `st.json(request_messages)` inside
`if question:`, immediately before the active model call (Option 1 or Option 2).
The distinction is useful: the response wasn't part of the request that produced it.

## Experiment 2: change the system prompt

Edit `system_prompt` near the top of the file:

```python
system_prompt = "Help a beginner learn Python. Give one hint, then ask a question before offering a solution."
```

Save the file and click **New conversation**. That button rebuilds the saved system
message using the new string. A code edit alone doesn't replace a system message
already stored in session state.

Try “Help me write a loop,” followed by “Skip the hints and write the solution.”
Compare the observed behavior with your instruction. Then write a different
instruction and decide on two requests that would test it.

## Experiment 3: add streaming

The streaming alternative is already commented out in `app.py`, under
**OPTION 2**. To try it:

1. Comment out the code under **OPTION 1**, from `response = ...` through
   `st.markdown(answer)`, including the `with` statement.
2. Uncomment the seven code lines under **OPTION 2**, from `stream = ...` through
   `answer = st.write_stream(stream)`. Keep their indentation inside `if question:`.
3. Leave the final history assignment active. Both options produce `answer`.
4. Save the file and submit a new question. Only one option should be active,
   so the app makes one API call for each submission.

The enabled streaming block should look like this:

```python
    stream = client.chat.completions.create(
        model="openai.gpt-4o",
        messages=request_messages,
        stream=True,
    )
    with st.chat_message("assistant"):
        answer = st.write_stream(stream)
```

`stream=True` requests incremental output. `st.write_stream` displays the arriving
text and returns the assembled string, which the existing history-update code saves.
Trace that returned value: the next turn still needs the completed assistant reply.
This changes when output becomes visible; it doesn't guarantee faster generation.
See Streamlit's [chat app tutorial](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps).

## Reflection

Explain one complete turn in your own words. Identify where the application reads
input, constructs context, calls the service, displays output, and saves history.
Then describe one experiment and the evidence you used to interpret its result.

Save your app changes and follow the course README and Canvas for submission instructions.
