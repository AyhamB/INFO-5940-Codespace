"""
INFO 5940 - Streamlit Primer
Progressive Uncommenting Exercises

How this works:
1. Read INFO_5940_Streamlit_Primer.md
2. Find each section mentioned (e.g., "Section 1.1")
3. Uncomment that section's code below
4. Save and watch your app update
5. Move to the next section

Goal: by the end, you'll have the core Streamlit patterns needed for chatbot-style AI apps.
"""

from pathlib import Path
import json
import time
import streamlit as st

# ============================================
# PART 0: PAGE CONFIGURATION + BRANDING
# ============================================

# ====== SECTION 0.1: Page Configuration ======
# 📝 Read Section 0.1 in the .md file, then uncomment below:
# Put st.set_page_config(...) near the top, before other UI-rendering st.* calls.

# st.set_page_config(
#     page_title="INFO 5940 Streamlit Primer",
#     page_icon="📚",
#     layout="centered",
# )

# ====== SECTION 0.2: Cornell Header (Columns) ======
# 📝 Read Section 0.2 in the .md file, then uncomment below:

# col1, col2 = st.columns([1, 4])
# with col1:
#     st.image(
#         str(Path(__file__).resolve().parent / "assets" / "cornell_seal.png"),
#         width=100,
#     )
# with col2:
#     st.markdown(
#         "<h3 style='color: #b31b1b; margin-bottom: 0;'>📚 Streamlit Primer</h3>",
#         unsafe_allow_html=True,
#     )
#     st.caption("Powered by INFO 5940")
#
# st.markdown("---")

# ============================================
# PART 1: UI ELEMENTS
# ============================================

# ====== SECTION 1.1: Display Text ======
# 📝 Read Section 1.1 in the .md file, then uncomment below:

# st.title("📚 Streamlit Primer: Progressive Learning")
# st.header("This is a header")
# st.subheader("And this is a subheader")
# st.caption("Uncomment sections as you learn!")
# st.write("This is regular text displayed with st.write()")
#
# st.markdown("---")

# ====== SECTION 1.2: Markdown Formatting ======
# 📝 Read Section 1.2 in the .md file, then uncomment below:

# st.markdown("**Bold text** and *italic text* with Markdown")
# st.markdown("- Bullet point 1\n- Bullet point 2")
#
# st.markdown(
#     "<h5 style='text-align: center; color: #4CAF50;'>🤖 HTML Styled Title</h5>",
#     unsafe_allow_html=True,
# )
#
# st.markdown("---")

# ====== SECTION 1.3: Info Boxes ======
# 📝 Read Section 1.3 in the .md file, then uncomment below:

# st.info("ℹ️ This is an informational message")
# st.success("✅ This is a success message")
# st.warning("⚠️ This is a warning message")
# st.error("❌ This is an error message")
#
# st.markdown("---")

# ====== SECTION 1.4: Chat Messages ======
# 📝 Read Section 1.4 in the .md file, then uncomment below:

# st.subheader("Chat Interface Components")
# st.chat_message("assistant").write("👋 I'm an assistant message!")
# st.chat_message("user").write("And I'm a user message!")
#
# st.markdown("---")

# ============================================
# PART 2: INTERACTIVITY (WIDGETS)
# ============================================

# ====== SECTION 2.1: Text Input ======
# 📝 Read Section 2.1 in the .md file, then uncomment below:

# st.header("Part 2: Interactivity")
# name = st.text_input("What's your name?")
# if name:
#     st.write(f"Nice to meet you, {name}!")
#
# st.markdown("---")

# ====== SECTION 2.2: Buttons ======
# 📝 Read Section 2.2 in the .md file, then uncomment below:

# if st.button("👋 Click Me"):
#     st.write("Button was clicked!")
#
# st.markdown("---")

# ====== SECTION 2.3: Chat Input ======
# 📝 Read Section 2.3 in the .md file, then uncomment below:

# if test_prompt := st.chat_input("Test the chat input..."):
#     st.write(f"You typed: {test_prompt}")
#
# st.markdown("---")

# ====== SECTION 2.4: File Uploader ======
# 📝 Read Section 2.4 in the .md file, then uncomment below:

# st.subheader("Upload a file")
# uploaded_file = st.file_uploader("Upload a document", type=["pdf", "txt", "md"])
#
# if uploaded_file is not None:
#     st.success("✅ File uploaded!")
#     st.write("Filename:", uploaded_file.name)
#
# st.markdown("---")

# ============================================
# PART 3: THE "AHA!" MOMENT — RERUNS
# ============================================

# ====== SECTION 3.1: Rerun Meter ======
# 📝 Read Section 3.1 in the .md file, then uncomment below:
# Interact with ANY widget below and watch the rerun counter increase!

# st.header("Part 3: The 'Aha!' Moment — Reruns")
#
# st.subheader("🔁 Rerun Meter: See Reruns in Action")
#
# # Initialize rerun counter
# if "_run_count" not in st.session_state:
#     st.session_state._run_count = 0
#
# st.session_state._run_count += 1
#
# # Display rerun stats in columns
# col1, col2 = st.columns(2)
# with col1:
#     st.metric("Total Reruns", st.session_state._run_count)
# with col2:
#     st.caption(f"Last rerun: {time.strftime('%H:%M:%S')}")
#
# st.markdown("---")
# st.write("**Try interacting with these widgets and watch the rerun counter increase:**")
#
# # Multiple widgets to interact with
# col_a, col_b = st.columns(2)
#
# with col_a:
#     st.button("🔘 Click Me")
#
# with col_b:
#     st.slider("Slide me", 0, 10, 5, key="rerun_test_slider")
#
# st.markdown("---")
#
# st.success(
#     """
#     **What's happening?**
#
#     Every time you interact with ANY widget, Streamlit reruns this entire script from top to bottom.
#     The counter increases because we increment it on every run. Watch how:
#     - Clicking the button → rerun!
#     - Moving the slider → rerun!
#
#     This is Streamlit's core behavior. Now let's see why this matters...
#     """
# )
#
# st.markdown("---")

# ====== SECTION 3.2: The Broken Counter ======
# 📝 Read Section 3.2 in the .md file, then uncomment below:
# Click the button multiple times and observe what happens!

# st.subheader("The Broken Counter")
# st.write("Let's build a counter. Click the button multiple times...")
#
# counter_broken = 0
#
# if st.button("🔢 Count (Broken)"):
#     counter_broken += 1
#
# st.write(f"Broken Counter: {counter_broken}")
#
# st.error(
#     """
#     🤔 **Why does it always show 1?**
#
#     Every button click reruns the entire script!
#     1. Script starts
#     2. `counter_broken = 0` ← Reset!
#     3. Click → `counter_broken += 1`
#     4. Shows 1
#     5. Next click → Back to step 1!
#
#     The counter never accumulates to 2, 3, 4... because regular variables don't persist across reruns.
#     """
# )
#
# st.markdown("---")

# ====== SECTION 3.3: Buttons vs Checkboxes ======
# 📝 Read Section 3.3 in the .md file, then uncomment below:

# st.subheader("Buttons vs Checkboxes: Events vs State")
#
# clicked = st.button("Click (event)")
# agreed = st.checkbox("I agree (state)")
#
# st.write("Button clicked this run?", clicked)
# st.write("Checkbox currently checked?", agreed)
#
# st.markdown("---")

# ============================================
# PART 4: SESSION STATE & ARCHITECTURE
# ============================================

# ====== SECTION 4.1: Session State Basics ======
# 📝 Read Section 4.1 in the .md file, then uncomment below:
# This fixes the counter using session state!

# st.header("Part 4: Session State — The Solution")
#
# if "counter" not in st.session_state:
#     st.session_state.counter = 0
#
# if st.button("🔢 Count (Working)"):
#     st.session_state.counter += 1
#
# st.write(f"Working Counter: {st.session_state.counter}")
# st.success("✅ Session state persists across reruns!")
#
# st.markdown("---")

# ====== SECTION 4.2: The Rerun Model Explained ======
# 📝 Read Section 4.2 in the .md file, then uncomment below:

# st.subheader("Understanding the Rerun Model")
# st.info(
#     "Every interaction causes Streamlit to rerun your script from top to bottom.\n\n"
#     "Your UI is rebuilt each time from the `st.*` calls in your code.\n\n"
#     "`st.session_state` is how you keep values around between reruns."
# )
#
# st.markdown("---")

# ====== SECTION 4.3: About st.rerun() ======
# 📝 Read Section 4.3 in the .md file
# Note: This is an informational section - no code to uncomment here!
# st.rerun() is available when you need to force an immediate refresh,
# but for most apps in this course, you won't need it.

# ============================================
# PART 5: LAYOUTS
# ============================================

# ====== SECTION 5.1: Columns ======
# 📝 Read Section 5.1 in the .md file, then uncomment below:

# st.header("Part 5: Layouts")
# st.subheader("Columns")
#
# col1, col2, col3 = st.columns(3)
#
# with col1:
#     st.write("**Column 1**")
#     st.write("Equal width")
#
# with col2:
#     st.write("**Column 2**")
#     st.write("Equal width")
#
# with col3:
#     st.write("**Column 3**")
#     st.write("Equal width")
#
# col_wide, col_narrow = st.columns([2, 1])
# with col_wide:
#     st.write("**Wide Column** (2x)")
# with col_narrow:
#     st.write("**Narrow** (1x)")
#
# st.markdown("---")

# ====== SECTION 5.2: Sidebar ======
# 📝 Read Section 5.2 in the .md file, then uncomment below:

# with st.sidebar:
#     st.header("⚙️ Sidebar Settings")
#     st.write("This content appears in the sidebar!")
#
#     if "counter" in st.session_state:
#         st.write(f"**Counter Value:** {st.session_state.counter}")
#
#     st.markdown("---")
#
# st.markdown("---")

# ============================================
# PART 6: THE COMPLETE CHATBOT PATTERN
# ============================================

# ====== SECTION 6.1: Initialize Message History ======
# 📝 Read Section 6.1 in the .md file, then uncomment below:

# st.header("Part 6: Complete Chatbot")
#
# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {"role": "assistant", "content": "Hello! How can I help you today?"}
#     ]

# ====== SECTION 6.2: Display Message History ======
# 📝 Read Section 6.2 in the .md file, then uncomment below:

# for msg in st.session_state.get("messages", []):
#     st.chat_message(msg["role"]).write(msg["content"])

# ====== SECTION 6.3: Capture User Input ======
# 📝 Read Section 6.3 in the .md file, then uncomment below:

# if prompt := st.chat_input("Type your message here...", key="chatbot_input"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)

# ====== SECTION 6.4: Generate and Display Response ======
# 📝 Read Section 6.4 in the .md file, then uncomment below:
# Note: In the chatbot activity, you'll learn to connect this to OpenAI's API for real AI responses.
# For now, we'll just echo back what the user says to demonstrate the pattern.

#     # For now, create a simple echo response
#     # (In the chatbot activity, you'll replace this with OpenAI API calls)
#     response = f"You said: {prompt}"
#
#     # Display the response
#     st.chat_message("assistant").write(response)
#
#     # Add assistant response to history
#     st.session_state.messages.append({"role": "assistant", "content": response})

# ============================================
# PART 7: ADDITIONAL COMPONENTS
# ============================================

# ====== SECTION 7.1: Spinners and Stop ======
# 📝 Read Section 7.1 in the .md file, then uncomment below:

# st.header("Part 7: Additional Components")
# st.subheader("Spinners + Stop")
#
# uploaded = st.file_uploader("Upload something (optional)", type=["txt"], key="spinner_upload")
#
# if uploaded is None:
#     st.warning("Upload a file to continue below.")
#     st.stop()
#
# with st.spinner("Processing..."):
#     time.sleep(2)
# st.success("Done!")
#
# st.markdown("---")

# ====== SECTION 7.2: Dynamic Updates with st.empty() ======
# 📝 Read Section 7.2 in the .md file, then uncomment below:

# st.subheader("Dynamic Updates with st.empty()")
#
# if st.button("▶️ Run Dynamic Update"):
#     placeholder = st.empty()
#     for i in range(5):
#         placeholder.info(f"Step {i+1}/5...")
#         time.sleep(0.5)
#     placeholder.success("All steps complete!")
#
# st.markdown("---")

# ====== SECTION 7.3: Display Helpers ======
# 📝 Read Section 7.3 in the .md file, then uncomment below:

# st.subheader("Display Helpers")
# st.json({"status": "ok", "items": [1, 2, 3]})
# st.code("print('Hello from code block')", language="python")
#
# st.markdown("---")

# ====== SECTION 7.4: Download Button ======
# 📝 Read Section 7.4 in the .md file, then uncomment below:

# st.subheader("Download Button")
# content = json.dumps({"message": "Thanks for learning Streamlit!"}, indent=2)
# st.download_button("Download JSON", data=content, file_name="example.json", mime="application/json")
#
# st.markdown("---")

# ============================================
# COMPLETION MESSAGE + FOOTER
# ============================================

st.markdown("---")

st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "INFO 5940 Streamlit Primer<br>"
    "For assistance, contact course staff"
    "</div>",
    unsafe_allow_html=True,
)
