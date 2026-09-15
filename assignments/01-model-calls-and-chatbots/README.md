# Model Calls, Instructions, and Chatbots

**INFO 5940 · 75-minute hands-on session**

Open [workbook.ipynb](workbook.ipynb) and work through it from top to bottom.
Run the code cells in order. At each **Your turn** activity, try the suggested
changes and record your predictions and observations in the notebook.

The [standalone Streamlit activity](STREAMLIT.md) has its own instructions.
You can launch the app without running the notebook.

## Streamlit primer

For a step-by-step introduction to Streamlit, use the
[INFO 5940 Streamlit Primer](streamlit-primer/INFO_5940_Streamlit_Primer.md) and its
[companion Python file](streamlit-primer/INFO_5940_Streamlit_Primer.py). Uncomment the exercises
as you read. The primer ends with an echo chatbot and needs no model API key.

From the repository root:

```bash
streamlit run assignments/01-model-calls-and-chatbots/streamlit-primer/INFO_5940_Streamlit_Primer.py
```

Stop the primer with **Ctrl+C** before launching `app.py` for the model-backed chatbot.

## What you will do

1. Read an API reference and inspect a model call.
2. Change application instructions and connect the experiment to the Model Spec.
   Inspect the knowledge cutoff and test answers with and without supplied source text.
3. Build conversation history and inspect tokens with `tiktoken`.
4. Compare direct and chain-of-thought prompts; optionally explore reasoning effort
   through the Responses API.
5. Explore a working Streamlit chatbot in a separate activity.

Run the app from the repository root:

```bash
streamlit run assignments/01-model-calls-and-chatbots/app.py
```

The app is a compact, commented example with an explicit system prompt, conversation history,
and model call. [STREAMLIT.md](STREAMLIT.md) explains the code and guides you through the exercises. Start with the basic
chatbot, then use the guide's small code extensions to inspect messages and add
streaming. After editing `system_prompt`, click **New conversation** to apply it.

## References

- [Chat Completions reference](https://developers.openai.com/api/reference/python/resources/chat/subresources/completions/methods/create)
- [Responses reference](https://developers.openai.com/api/reference/python/resources/responses/methods/create)
- [Model Spec: August 18, 2026 edition](https://model-spec.openai.com/2026-08-18.html#instructions-and-levels-of-authority)
- [Reasoning models](https://developers.openai.com/api/docs/guides/reasoning)
- [Conversation state](https://developers.openai.com/api/docs/guides/conversation-state?api-mode=chat)
- [Interactive tokenizer](https://platform.openai.com/tokenizer)

Save and push your work following the course README; follow Canvas for submission
instructions.
