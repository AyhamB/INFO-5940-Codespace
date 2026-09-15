# INFO 5940 Streamlit Primer

Welcome to the INFO 5940 Streamlit Primer. This hands-on primer teaches *just enough* Streamlit to build the AI chatbot apps in this course. It's designed to be a fast, hands-on introduction, and not a full Streamlit course.

**Even if you have Python experience**, we suggest completing this primer as it introduces Streamlit's unique framework.

> **Tip:** The Streamlit framework is very well documented, with a vibrant community. We encourage you to explore these resources to supplement your learning.

---

## How to run a Streamlit app

A Streamlit "app" is just a regular Python `.py` file that Streamlit runs as a web app in your browser. Instead of printing values to the terminal, your code calls Streamlit functions (like `st.write`, `st.button`, `st.chat_message`) to build the UI.

To launch an app (i.e., run a Streamlit `.py` file), open a terminal window and run:

```bash
streamlit run filename.py
```

Replace `filename.py` with the file name of your app. Note: you must either provide the full/relative path to the file, or run the command from the folder where the file exists.

When you run this command, Streamlit starts a local server and opens the app in a browser tab.

---

## Development flow (save → rerun → see changes)

Streamlit is designed for a fast, interactive loop:

1. Edit the `.py` file
2. Save
3. Streamlit detects the change and prompts you to rerun
4. (Optional) Choose **"Always rerun"** (top-right in the app) to automatically rerun after every save

That is a quick and interactive loop, where you write a small change, save, see it live, then repeat until you're happy with how your app looks and behaves. This makes Streamlit pleasant to work with for AI Engineers.

> **Pro tip:** Arrange your code editor and browser (where the Streamlit app will be open) side-by-side to see updates in real-time.

---

## Learning approach for this primer

This primer uses two files:

- `INFO_5940_Streamlit_Primer.md` (this guide)
- `INFO_5940_Streamlit_Primer.py` (the Streamlit app you run)

You will uncomment code blocks progressively in the `.py` file while reading this guide.

**Workflow:**
1. Read the next numbered section below (e.g., "Section 1.1")
2. Find that same section in `INFO_5940_Streamlit_Primer.py` file
3. Uncomment the code block
4. Save the file and watch the app update
5. Repeat for subsequent sections

**Note:** Once you uncomment a section, leave it uncommented. Your app grows progressively - by the end of the primer, all sections will be uncommented and you'll have a complete, working chatbot.

---

## The 3 core ideas that power the Streamlit framework

Before we start, here's the mental model that will make everything click:

### 1) Your .py script *is* the UI
Every time your script runs, each `st.*` call adds something to the page, in order, from top to bottom.
Think of it like *"printing to the browser."*

### 2) Widgets return values
When you create a widget (like `st.text_input(...)`), it returns a value representing the user's current input. You can use that return value in your Python logic, and any API calls that you make. Typically you would assign this value to a variable.

### 3) Streamlit reruns your script each time
Each user interaction (click, typing, uploading a file, etc.) triggers a rerun **top-to-bottom**.
If you want data to persist between reruns, you use **`st.session_state`**.

You'll see all three ideas come together in the next few sections.

---

# Part 0: Basic Streamlit app structure

Most Streamlit apps follow a common structure:

1. Python Library Imports at the top (e.g., `streamlit`, `openai`, etc.)
2. Page configuration near the top, which is set using `st.set_page_config`
3. Layout skeleton (header, columns, sidebar)
4. Widgets and logic, for handling inputs and responses
5. Persistent state across reruns, which are set using `st.session_state`

### Streamlit import convention

Streamlit is typically imported as:

```python
import streamlit as st
```

That `as st` is just a Python alias. It means Streamlit capabilities are prefixed with `st`, and you use the dot operator (`.`) to access them, like `st.write(...)`, `st.button(...)`, etc., throughout the script.

---

## Before You Begin: Launch the App

Even though most of the code is commented out, go ahead and launch the Streamlit app from the repository root now:

```bash
  streamlit run assignments/01-model-calls-and-chatbots/streamlit-primer/INFO_5940_Streamlit_Primer.py
```

What you'll see is a mostly blank page. This is completely normal!

What happens next: As you read through each section in this guide, you'll uncomment the corresponding code in the .py file. Each time you save, the app updates in your browser. By the end, you'll have a fully functional chatbot.

Important: Once you uncomment a section, leave it uncommented. Your app builds progressively, with each new section adding to what came before.

## Section 0.1: Page configuration

`st.set_page_config()` controls the page title, icon, and layout. A typical pattern looks like:

```python
st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
    layout="centered",  # or "wide"
)
```
When users open your app in their browser, `page_title` is what appears in the browser tab. The `page_icon` shows up next to the title (you can use emojis or image URLs). The `layout` parameter controls whether content is centered in the middle of the page or spreads across the full width.

**Commonly used parameters:**
- `page_title`: String that appears in the browser tab
- `page_icon`: Emoji (like "🤖") or URL to an icon image
- `layout`: Either "wide" (full width) or "centered" (default, narrower)

**Important practical note:** put `st.set_page_config(...)` near the top of your script **before other `st.*` calls that render UI**. If you place it later, Streamlit may warn/error and ask you to move it.

📝 **Action:** Look at Section 0.1 in the `.py` file, uncomment the lines of code, and observe the changes to the app in the browser. Note that this change is rather subtle, and you can see that title of the browser tab may have changed to say "INFO 5940 Streamlit Primer", and it also has the book emoji at the beginning. 

---

## Section 0.2: Cornell-style header (columns)

A branded header can be built with columns:

- `st.columns(...)` creates side-by-side areas
- `with col:` sends UI calls into that column

Example:

```python
from pathlib import Path

col1, col2 = st.columns([1, 2.5])

with col1:
    st.image(str(Path(__file__).resolve().parent / "assets" / "cornell_seal.png"), width=120)

with col2:
    st.markdown("<h3 style='color: #b31b1b;'>🤖 My App</h3>", unsafe_allow_html=True)
    st.caption("Powered by INFO 5940")
```

Here, `st.columns()` takes the values [1, 2.5], indicating that we need two columns, where the second one is 2.5 times the width of the first one.

📝 **Action:** Look at Section 0.2 in the `.py` file, uncomment the lines of code, and observe the changes to the app in the browser. Notice how `with col1:` / `with col2:` blocks work to showcase an image and text side-by-side. You will learn more about `st.markdown()` and `st.caption()` shortly. For now, focus on the layout. 

---

# Part 1: UI elements (display)

Streamlit makes it incredibly easy to display content on the screen. In this part, you'll learn the fundamental building blocks for creating your user interface. 

---

## Section 1.1: Displaying text

Streamlit provides several text display functions, each with a different visual weight and purpose. These are similar to the `print()` and `display()` functions you've seen in Python notebooks, but designed for web interfaces:

```python
st.title("My App Title")           # Large heading
st.header("Section Header")        # Medium heading
st.subheader("Subsection")         # Smaller heading
st.caption("Small gray text")      # Tiny caption
st.write("Regular text")           # Versatile display function
```

**When to use each:**
- `st.title()`: The main headline of your page; use it just once at the top
- `st.header()`: Major section breaks (like "Part 1: Setup" or "Part 2: Results")
- `st.subheader()`: Subsections within a major section
- `st.caption()`: Small supplementary text (like "Last updated: ..." or "Source: ...")
- `st.write()`: Use it for displaying almost anything in a regular font size

**`st.write()` is special** - it's smart about what you pass it:
- Text string → displays as text
- DataFrame → renders as an interactive table
- Chart object → shows the chart
- Dictionary → displays as JSON
- Markdown string → formats it with bold, italics, etc.

If you're ever unsure what to use, start with `st.write()`.

```python
# All of these work with st.write()!
st.write("Plain text")
st.write({"name": "Alice", "age": 30})  # Shows as formatted JSON
st.write(dataframe)  # Shows as interactive table
st.write("**Bold** and *italic*")  # Markdown formatting
```

> **Note:** `st.write()` doesn't support `unsafe_allow_html=True` for custom HTML. Use `st.markdown()` when you need that feature.

📝 **Action:** Uncomment **Section 1.1** in the `.py` file, and observe the different ways of displaying text on the screen.

---

## Section 1.2: Markdown formatting

Markdown is a simple way to add formatting to your text without writing HTML. Streamlit fully supports Markdown syntax through `st.markdown()`:

```python
st.markdown("**Bold text** and *italic text*")
st.markdown("- Bullet points\n- Are easy")
```

You can also use simple HTML for styling (sparingly):

```python
st.markdown(
    "<h3 style='text-align: center; color: #4CAF50;'>🤖 HTML Styled Title</h3>",
    unsafe_allow_html=True
)
```

**Basic Markdown syntax:**

```python
st.markdown("**Bold text** and *italic text*")
st.markdown("- Bullet point 1\n- Bullet point 2")
st.markdown("1. Numbered item\n2. Another item")
st.markdown("[Link text](https://example.com)")
st.markdown("`code text`")
```

**Custom HTML styling:**

Sometimes you need more control over appearance. Streamlit allows you to inject custom HTML and CSS, though use this sparingly:

```python
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>
         HTML Styled Title
    </h1>
""", unsafe_allow_html=True)
```

**Why use HTML/CSS in Streamlit?** When you need precise control over colors, alignment, fonts, or spacing that Markdown doesn't provide. Common use cases:
- Centered, colored titles
- Custom spacing between elements
- Styled containers or boxes
- Brand-specific fonts or colors

**Safety note:** The `unsafe_allow_html=True` parameter is required to render HTML. It's called "unsafe" because in production apps, you should be careful about injecting user-provided HTML (security risk). For your own code, it's perfectly fine.

**📝 Action:** Uncomment **Section 1.2** in the `.py` file and see the difference between plain Markdown and HTML-styled content!

---

## Section 1.3: Info boxes

Info boxes are colored, styled containers that draw attention to important messages. They're perfect for status updates, warnings, errors, or helpful tips:

```python
st.info("ℹ️ Informational message")
st.success("✅ Success message")
st.warning("⚠️ Warning message")
st.error("❌ Error message")
```

**When to use each type:**
- **`st.info()`**: Blue box - neutral information, tips, or explanations
  - Example: "Tip: Click 'Always rerun' in the top-right corner"
- **`st.success()`**: Green box - successful operations or positive confirmations
  - Example: "✅ File uploaded successfully!"
- **`st.warning()`**: Yellow box - cautions or things to be aware of
  - Example: "⚠️ This action cannot be undone"
- **`st.error()`**: Red box - errors, failures, or critical issues
  - Example: "❌ Failed to connect to API. Check your credentials."

**Best practices:**
- Add emojis at the start for visual reinforcement (ℹ️ ✅ ⚠️ ❌)
- Keep messages concise and actionable
- Use them sparingly - too many colored boxes become visual noise
- Consider combining with `st.stop()` after errors to halt execution

These are great in AI apps for status updates and guardrails (e.g., "missing API key").

📝 **Action:** Uncomment **Section 1.3** in the `.py` file. The `.py` file shows all four types. Notice how each has a different color and implied urgency!

---

## Section 1.4: Chat messages

Streamlit has specialized components specifically designed for chat interfaces. These are crucial for building chatbots because they automatically style messages with appropriate avatars and formatting.

```python
st.chat_message("assistant").write("Hello! I'm an AI assistant.")
st.chat_message("user").write("Hi there!")
```

**How it works:**
- `st.chat_message(role)` creates a container with an avatar on the left
- Everything inside the container (using `.write()`, `.markdown()`, etc.) appears in a chat bubble
- The role determines which avatar is shown

**Available roles:**
- `"assistant"` → Robot/AI icon (🤖) - used for bot responses
- `"user"` → Person icon (👤) - used for user messages
- `"ai"` → Same as assistant
- `"human"` → Same as user
- Any custom string → Generic icon (unless you provide a custom avatar)

**Custom avatars:**
```python
st.chat_message("assistant", avatar="🦙").write("I'm a llama assistant!")
st.chat_message("user", avatar="👩‍💻").write("Custom user icon")
```

**Important for chatbots:** These components are designed to be used in a loop. You'll typically iterate through a list of messages and display each one with the appropriate role. We'll see this pattern below when we build the complete chatbot.

**📝 Action:** Uncomment **Section 1.4** in the `.py` file, and see the chat message examples. Notice the automatic styling and avatars!

---

# Part 2: Interactivity (widgets)

Now let's make things respond to user actions! While Part 1 was about displaying information, Part 2 is about capturing input and making your app interactive. Think of these as the "verbs" of your app, i.e,. the actions users can take.

Widgets are how users interact with your app. Most widgets follow the same pattern:

1. You create the widget
2. Streamlit returns a value
3. You react to that value in Python

---

## Section 2.1: Text input

Text input widgets let users type and submit text. This is your basic form input.

```python
name = st.text_input("What's your name?")
if name:
    st.write(f"Nice to meet you, {name}!")
```

1. `st.text_input()` displays a text box with a label
2. As the user types, the text is captured but doesn't trigger a rerun yet
3. When the user presses **Enter** or clicks away from the input box, Streamlit reruns and stores the value in `name`
4. You can check if they've entered anything with `if name:` (empty strings are false)

**Common use cases:**
- Name or email input
- Search boxes
- API key entry
- Short text responses

**Additional parameters:**
```python
password = st.text_input("Password", type="password")  # Hides text
api_key = st.text_input("API Key", placeholder="Enter your key...")
multi_line = st.text_area("Tell me more...")  # For longer text
```

📝 **Action:** Uncomment **Section 2.1** in the `.py` file. Type your name (notice nothing happens yet), then press **Enter** or click outside the input box to see the greeting appear. 

---

<!-- ## Section 2.2: Buttons

Buttons let users trigger actions. They're the most common way to let users say "yes, do this now." They return `True` only on the rerun where they were clicked.

```python
if st.button("Click Me"):
    st.write("Button was clicked!")
```

**Critical understanding:** The `if` block **only executes when the button is clicked**. This is different from text inputs that update continuously. Let's see why this matters:

```python
# This message ONLY appears when button is clicked
if st.button("Say Hello"):
    st.write("Hello!")  # Appears only in the current run, and will disappear on the next run
```

**Why does the message disappear?** Because of Streamlit's rerun model:
1. User clicks button → button returns `True` → message shows → page reruns
2. After rerun, button is no longer clicked → button returns `False` → message doesn't show

We'll explore this more below, but for now, remember that buttons return `True` only during the rerun in which they were clicked.

**Styled buttons:**
```python
if st.button("Primary Action", type="primary"):  # Blue, prominent
    st.write("Primary button clicked!")

if st.button("Delete", type="secondary"):  # Default gray
    st.write("Secondary button clicked!")
```

**Common use cases:**
- Submit forms
- Trigger computations
- Confirm actions
- Reset state
- Download results

This is important: **buttons don't "stay True."**
If you need long-lived values (like counters, chat history, settings), they need to be stored them in `st.session_state`. We will read about this below.

📝 **Action:** Uncomment **Section 2.2** in the `.py` file, and try clicking the button. Once you see the message *"Button was clicked!"*, go back to the name input text box from the previous section, and enter another name there. Notice how the message now disappears!

**Why does it disappear?** The button only returns `True` during the rerun where it was clicked. When you typed in the name input, that triggered a new rerun - but this time, the button wasn't clicked, so the message doesn't appear. This is Streamlit's rerun model in action! -->

---

## Section 2.2: Buttons

Buttons let users trigger actions. They're the most common way to let users say "yes, do this now." They return `True` only on the rerun where they were clicked.

```python
if st.button("Click Me"):
    st.write("Button was clicked!")
```

**Critical understanding:** The `if` block only executes when the button is clicked.

**Styled buttons:**
```python
if st.button("Primary Action", type="primary"):  # Blue, prominent
    st.write("Primary button clicked!")

if st.button("Delete", type="secondary"):  # Default gray
    st.write("Secondary button clicked!")
```

**Common use cases:**
- Submit forms
- Trigger computations
- Confirm actions
- Reset state
- Download results

**Important:** Buttons don't "stay True." If you need long-lived values (like counters, chat history, settings), store them in `st.session_state` (we'll learn about this below).

📝 **Action:** Uncomment Section 2.2 in the `.py` file, and try clicking the button. Once you see the message "Button was clicked!", go back to the name input text box from the previous section, and enter another name there. Notice how the message now disappears!

**Why does it disappear?** The button only returns `True` during the rerun where it was clicked. When you typed in the name input, that triggered a new rerun - but this time, the button wasn't clicked, so the message doesn't appear. This is Streamlit's rerun model in action!

---

## Section 2.3: Chat input

`st.chat_input()` is a specialized widget designed specifically for chatbot interfaces. It looks like a message box at the bottom of the page to give the feeling of a messaging app. When the user submits, it returns the text on that rerun:

```python
if prompt := st.chat_input("Type your message..."):
    st.write(f"You typed: {prompt}")
```

This uses the **walrus operator** (`:=`), which assigns and check in one line of code.

```python
# Equivalent to:
prompt = st.chat_input("Message...")
if prompt:
    st.write(prompt)

# Same as:
if prompt := st.chat_input("Message..."):
    st.write(prompt)
```

Both do exactly the same thing:
1. Display the chat input widget
2. Store user input in `prompt`
3. Only execute the `if` block when user submits a message (presses Enter)

**Why is this useful?** In chatbots, you almost always want to:
1. Get the input
2. Immediately check if they entered something
3. Process it if they did

The walrus operator makes this pattern cleaner and more readable.

**Important behavior:** The chat input only triggers a rerun when the user presses Enter (or clicks the send icon), not while they're typing. This ensures you only process complete messages.

**Conditional enabling:**
You can disable the input until certain conditions are met (like a file being uploaded): 

**Disabling the input:**
```python
# Don't allow input until a file is uploaded
uploaded_file = st.file_uploader("Upload document")
if prompt := st.chat_input("Ask about the document", disabled=not uploaded_file):
    st.write(f"You asked: {prompt}")
```

📝 **Action:** Uncomment **Section 2.3** in the `.py` file. Notice how it stays at the bottom and only processes when you press Enter.

---

## Section 2.4: File uploader

Streamlit's file uploaders let users upload files from their computer. This is essential for many AI apps where users' files need to be processed.

```python
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "txt", "md"])

if uploaded_file is not None:
    st.success("✅ File uploaded!")
    st.write("Filename:", uploaded_file.name)
```

**How it works:**
1. `st.file_uploader()` displays a drag-and-drop zone or browse button
2. User uploads a file
3. The file object is stored in `uploaded_file` (or `None` if nothing uploaded)
4. You can access file properties and contents through this object

**File type filtering:**
```python
# Only accept PDFs
pdf_file = st.file_uploader("Upload PDF", type=["pdf"])

# Accept multiple formats
doc_file = st.file_uploader("Upload document", type=["pdf", "txt", "md", "docx"])

# Accept images
image_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg", "gif"])
```

**Accessing file contents:**

When you upload a file, Streamlit gives you raw bytes (binary data), not text. You need to decode it to get readable text:

```python
if uploaded_file:
    # Get raw bytes from the file
    raw_bytes = uploaded_file.read()  # Returns bytes like b'\x89PNG...'

    # Convert bytes to text string (for text files like .txt, .md, .csv)
    text = raw_bytes.decode("utf-8")

    # Now you can work with the text
    st.write(text)
```

**What's happening:**
- `uploaded_file.read()` returns bytes (raw binary data)
- `.decode("utf-8")` converts bytes to a text string using UTF-8 encoding
- UTF-8 is the most common text encoding that supports all languages and special characters

**Handling encoding errors:**

Sometimes files have characters that can't be decoded. Use `errors="ignore"` to skip them:

```python
text = raw_bytes.decode("utf-8", errors="ignore")  # Skips problematic characters
```

**Multiple files:**
```python
files = st.file_uploader("Upload files", type=["txt"], accept_multiple_files=True)
if files:
    for file in files:
        st.write(f"Processing {file.name}...")
```

**Important pattern:** Always check if a file was uploaded before trying to process it:
```python
uploaded_file = st.file_uploader("Upload document")

if not uploaded_file:
    st.info("Please upload a file to continue")

# Only runs if file is uploaded
content = uploaded_file.read().decode("utf-8")
st.write(content)
```

📝 **Action:** Uncomment **Section 2.4** in the `.py` file. Try uploading a file using the uploader. See how it displays the filename and size!

---

# Part 3: The "Aha!" moment — reruns

This is the most important section of the primer. Understanding this concept is essential for everything that follows. We're going to build something that seems like it should work... but doesn't. This will reveal Streamlit's fundamental behavior.

> **When users interact with widgets, Streamlit reruns your script from top to bottom.**

This is what makes Streamlit feel "live"… and it's also why normal variables don't persist.

---

## Section 3.1: A rerun meter (watch it tick)

Before we dive into the problem, let's *see* reruns in action.

In the `.py` file, you'll uncomment an interactive "rerun meter" that shows:
- **Total reruns** - how many times your script has executed
- **Timestamp** - when the last rerun happened

You'll also get two widgets to interact with: a button and a slider.

📝 **Action:** Uncomment **Section 3.1** in the `.py` file. Now try:

1. **Click the button** - watch the rerun counter increase
2. **Move the slider** - counter increases again!
3. **Click the button again** - yet another rerun!
4. **Move the slider back and forth** - watch the counter go up each time!

**Notice:**
- The rerun counter keeps going up with every interaction
- The timestamp updates each time

**What's happening behind the scenes?**

Every single interaction causes Streamlit to run your entire script from top to bottom again. The counter increases because we increment it at the start of every run. This is Streamlit's fundamental behavior.

**Key insight:** Your script isn't running continuously in the background. It runs once, displays the UI, then waits. When you interact with something, it runs again from the beginning. This is what we mean by "reruns."

---

## Section 3.2: The broken counter

Now let's build something simple: a counter that increases each time you click a button.

```python
counter_broken = 0

if st.button("Count"):
    counter_broken += 1

st.write(f"Count: {counter_broken}")
```

**Expected behavior:** Click once → shows 1. Click again → shows 2. Click again → shows 3.

**Actual behavior:** It always shows 1, no matter how many times you click!

📝 **Action:** Uncomment **Section 3.2** in the `.py` file. Now **try it yourself** - click the button 5 times. 10 times. Try to make it count to 5. **It's impossible!** It's always stuck at 1.

### Why This Happens: The Rerun Model

This reveals Streamlit's core behavior. Let's trace through what happens, step by step, when you click the button:

**First click:**
```
1. Script starts running from line 1
2. counter_broken = 0           ← counter is 0
3. User clicks button
4. if st.button(...):           ← Returns True (button was just clicked)
5. counter_broken += 1          ← counter becomes 1
6. st.write(...)                ← Displays "Count: 1"
7. Script finishes
```

Great! It shows 1. Now let's click again:

**Second click:**
```
1. Script starts running from line 1 (STARTS OVER!)
2. counter_broken = 0           ← counter is back to 0!
3. User clicks button
4. if st.button(...):           ← Returns True (button was just clicked)
5. counter_broken += 1          ← counter becomes 1 again
6. st.write(...)                ← Displays "Count: 1"
7. Script finishes
```

**The key insight:** Each click causes a complete rerun from the beginning. The line `counter_broken = 0` executes again, resetting our counter. It increments to 1, but can never get to 2 because it keeps resetting.

### The Movie Analogy

Think of your Streamlit script like a movie:
- When you first open the app: The movie plays from beginning to end
- When you click a button: The movie **restarts from the beginning** and plays through again
- When you type in a text box: The movie **restarts from the beginning** and plays through again

Regular variables (like `counter_broken = 0`) are like actors changing costume - they reset every time the movie restarts. You can't rely on them to remember things between reruns.

### Why This Matters for Real Apps

Here's a more realistic example:

```python
# This seems like it should work, but doesn't
user_preferences = []

if category := st.selectbox("Pick a category", ["Sports", "News", "Tech"]):
    user_preferences.append(category)

st.write(f"You've selected {len(user_preferences)} categories")
```

**Problem:** The list resets to `[]` on every interaction. You can never build up a list of preferences because it keeps resetting.

### "Wait, Why Does Text Input Remember What I Typed?"

Good question! You might wonder: "If everything resets, how does `st.text_input()` remember what I typed?"

Streamlit's built-in widgets automatically store their values internally. When the script reruns, they restore their previous values. But **your variables** don't have this magic - they reset.

```python
# This works - text input remembers its value
name = st.text_input("Name")  # Streamlit remembers internally

# This doesn't work - counter resets
counter_broken = 0  # Always resets to 0
if st.button("Count"):
    counter_broken += 1
```

**The solution?** We need a way to explicitly tell Streamlit "remember this value between reruns." That's what `st.session_state` is for!

---

## Section 3.3: Buttons vs. checkboxes (events vs. state)

Before we learn the solution, here's one more important concept. Not all widgets behave the same way:

- **Buttons** are events: they're `True` only on the rerun where they were clicked
- **Checkboxes** represent state: once checked, they stay checked (until the user changes them)

```python
clicked = st.button("Click (event)")
agreed = st.checkbox("I agree (state)")

st.write("Button clicked this run?", clicked)
st.write("Checkbox currently checked?", agreed)
```

📝 **Action:** Uncomment **Section 3.3** in the `.py` file. Try clicking the button multiple times, and toggling the checkbox. Watch how:
- The button only shows `True` briefly (when clicked), then goes back to `False`
- The checkbox stays `True` or `False` based on its current state

**Why the difference?** Streamlit manages checkbox state internally (like text_input). But buttons are intentionally designed as events - they only fire once per click. For persistent data like counters, chat history, or settings, you need `st.session_state`.

---

# Part 4: Session state (the fix)

Now you understand the problem: variables reset on every rerun. Let's solve it! To persist values across reruns, Streamlit gives you `st.session_state`: a dict-like place to store values that should survive reruns for the user's session.

---

## Section 4.1: Session state basics (working counter)

`st.session_state` is a special dictionary that **persists across reruns**. Think of it as Streamlit's memory.

The standard pattern:

1. Initialize once (only if missing)
2. Update on interaction
3. Read and display

```python
if "counter" not in st.session_state:
    st.session_state.counter = 0

if st.button("Count"):
    st.session_state.counter += 1

st.write(st.session_state.counter)
```

**The difference:**
- Regular variable: `counter = 0` ← Resets every rerun
- Session state: `st.session_state.counter` ← Survives reruns

**Why the check?** If you just write `st.session_state.counter = 0` without the `if`, it will reset to 0 on every rerun - exactly the problem we're trying to avoid! The check ensures initialization only happens once.

📝 **Action:** Uncomment **Section 4.1** in the `.py` file.

---

## Section 4.2: The rerun model explained

Once you've felt it, here's the clean mental model:

- The browser shows widgets and sends widget values to the server
- The server runs your script top-to-bottom
- Your script regenerates the UI on every rerun
- `st.session_state` is your "memory" between reruns

### What triggers a rerun?

Almost any user interaction triggers an automatic rerun:

✅ `st.button()` - when clicked
✅ `st.text_input()` - when Enter is pressed or focus is lost
✅ `st.chat_input()` - when Enter is pressed
✅ `st.slider()` - while dragging
✅ `st.selectbox()` - when selection changes
✅ `st.checkbox()` - when toggled
✅ `st.file_uploader()` - when file is uploaded

You don't need to call anything - Streamlit does this automatically.

### The movie analogy

Think of your Streamlit script like a movie:
- When you first open the app: The movie plays from beginning to end
- When you click a button: The movie **restarts from the beginning** and plays through again
- When you type in a text box: The movie **restarts from the beginning** and plays through again

Regular variables (like `counter = 0`) are like actors changing costume - they reset every time the movie restarts. You can't rely on them to remember things between reruns.

### A detailed walkthrough

Let's trace through a complete example:

```python
st.title("My App")
name = st.text_input("Name")
age = st.number_input("Age", min_value=0, max_value=120)

if st.button("Submit"):
    st.write(f"{name} is {age} years old")
```

**When app first loads:**
```
Line 1: Display title "My App"
Line 2: Display empty text input, name = ""
Line 3: Display number input with value 0, age = 0
Line 4: Button not clicked, skip the if block
Script ends
```

**User types "Alice" in the name field:**
```
(Rerun triggered!)
Line 1: Display title "My App"
Line 2: Display text input with "Alice", name = "Alice"
Line 3: Display number input with value 0, age = 0
Line 4: Button not clicked, skip the if block
Script ends
```

Notice: Streamlit automatically restored "Alice" in the text input.

**User changes age to 25:**
```
(Rerun triggered!)
Line 1: Display title "My App"
Line 2: Display text input with "Alice", name = "Alice"
Line 3: Display number input with value 25, age = 25
Line 4: Button not clicked, skip the if block
Script ends
```

**User clicks Submit:**
```
(Rerun triggered!)
Line 1: Display title "My App"
Line 2: Display text input with "Alice", name = "Alice"
Line 3: Display number input with value 25, age = 25
Line 4: Button WAS clicked, enter if block
Line 5: Display "Alice is 25 years old"
Script ends
```

### Why this model is powerful

This might seem inefficient (rerun everything on every interaction?!), but it's actually brilliant:

1. **Simple mental model:** You write linear code, top to bottom, just like a regular Python script
2. **Everything stays in sync:** Every rerun rebuilds the entire page, so you never have stale UI
3. **Easy to reason about:** You can see exactly what the UI will look like by reading the code from top to bottom

### Performance Considerations

"But doesn't rerunning the entire script make it slow?"

In practice, no:
- Streamlit is optimized for this pattern
- Only changed elements are updated in the browser
- You can use `@st.cache_data` to cache expensive computations
- Most apps rerun in milliseconds

**📝 Action:** Read through the explanation in the `.py` file and see how it formalizes what you've experienced!

---

## Section 4.3: About `st.rerun()`

Most of the time, you don't need `st.rerun()` because widgets automatically trigger reruns when users interact with them.

However, Streamlit provides `st.rerun()` for situations where you need to manually force an immediate rerun:

```python
if st.button("Clear All Data"):
    st.session_state.clear()  # Clear all session state
    st.rerun()  # Immediately refresh to show clean state
```

**When it's useful:**
- After programmatically clearing or resetting session state
- In complex workflows where you need to force a refresh mid-execution
- When using callbacks or background operations

**Why you might not need it often:**
- Buttons, text inputs, and other widgets already trigger reruns
- Session state changes are visible on the next natural rerun
- It's usually cleaner to let Streamlit handle reruns automatically

For most chatbot and AI apps in this course, you won't need `st.rerun()`. Just know it exists if you ever need to force an immediate refresh.

---

# Part 5: Layouts (columns and sidebar)

Layouts help you organize your app so it's easy to use.

---

## Section 5.1: Columns

Columns split content side-by-side:

```python
col1, col2 = st.columns(2)

with col1:
    st.write("Left")

with col2:
    st.write("Right")
```

Custom widths:

```python
col_wide, col_narrow = st.columns([2, 1])
```

The numbers represent ratios:
- `[2, 1]` → left is 2/3 of the width, right is 1/3
- `[3, 1]` → left is 3/4 of the width, right is 1/4

**Common use cases:**
- Compact layouts
- Side-by-side comparisons
- Button rows
- Form layouts
- Dashboard metrics

📝 **Action:** Uncomment **Section 5.1** in the `.py` file.

---

## Section 5.2: Sidebar

The sidebar is perfect for settings and summary information:

```python
with st.sidebar:
    st.header("Settings")
```

Everything inside the `with st.sidebar:` block appears in the left sidebar. The sidebar can be collapsed by clicking the `<` icon that appears at the top right section of the column when you hover your cursor above it.

**Common sidebar patterns:**
- App settings (model, temperature, max tokens)
- Navigation
- Filters
- Status displays
- Reset buttons

📝 **Action:** Uncomment **Section 5.2** in the `.py` file.

---

# Part 6: The complete chatbot pattern

This is the core pattern for chatbot-style apps:

1. Initialize message history in `st.session_state`
2. Render the conversation
3. Capture user input
4. Generate and render assistant output

---

## Section 6.1: Initialize message history

```python
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]
```

**The data structure:**
Each message is a dictionary with two keys:
- `"role"`: Who sent the message (`"user"`, `"assistant"`, or `"system"`)
- `"content"`: The actual message text

**Why a list?** Because conversations are sequential - each message builds on previous ones.

**Why start with a greeting?** It's friendlier than an empty screen and shows users the chatbot is ready.

**The initialization pattern:** We check `if "messages" not in st.session_state` to ensure this only happens once, when the app first loads. On subsequent reruns, the message history persists.

**Example message history:**
```python
[
    {"role": "assistant", "content": "Hello! How can I help?"},
    {"role": "user", "content": "What's the weather?"},
    {"role": "assistant", "content": "I don't have access to weather data."},
    {"role": "user", "content": "Tell me a joke."},
    {"role": "assistant", "content": "Why did the Python programmer..."}
]
```

**📝 Action:** Uncomment Section 6.1 in the `.py` file to initialize the message history!

---

## Section 6.2: Display message history

Now we need to show all previous messages in the chat. We'll loop through the message history and display each one.

```python
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
```

**How this works:**
1. Loop through each message in the history
2. Use `st.chat_message()` to create a chat bubble with the appropriate role
3. Use `.write()` to display the message content

**Why does this work?** Remember the rerun model:
- Every time anything happens, the script runs from top to bottom
- This loop executes every time
- It displays ALL messages in the history
- Because history is in session state, it persists and grows

**The magic moment:**
1. User sends message → added to history → page reruns
2. Loop displays all messages including the new one
3. AI responds → added to history → page reruns
4. Loop displays all messages including AI response
5. History keeps growing!

**Example of what displays:**
```
🤖 Hello! How can I help you today?
👤 What's 2+2?
🤖 2+2 equals 4.
👤 Thanks!
🤖 You're welcome!
```

Each message automatically gets the right avatar (🤖 for assistant, 👤 for user) and styling.

**📝 Action:** Uncomment Section 6.2 in the `.py` file. You should now see the initial greeting message displayed!

---

## Section 6.3: Capture user input

Now let's handle new user input. When the user types a message and presses Enter, we need to:
1. Add their message to history
2. Display it immediately

```python
if prompt := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    st.chat_message("user").write(prompt)
```

**Step-by-step breakdown:**

**1. Capture input:**
```python
if prompt := st.chat_input("Type your message here..."):
```
- Displays the chat input box at the bottom of the page
- Waits for user to type and press Enter
- If they do, `prompt` contains their message and we enter the `if` block

**2. Save to history:**
```python
st.session_state.messages.append({"role": "user", "content": prompt})
```
- Create a message dictionary with role "user" and their message
- Append it to the messages list in session state
- Now it's permanently stored (until the session ends)

**3. Display immediately:**
```python
st.chat_message("user").write(prompt)
```
- Show the user's message right away
- This creates the chat bubble with user avatar
- Provides immediate feedback that their message was received

**Why display if we're already looping in 6.2?** Great question! We display here for immediate feedback. On the next rerun, the loop in 6.2 will display it again, but users see it instantly rather than waiting for the AI response.

**What happens next:**
1. User types "Hello" and presses Enter
2. Script reruns (because chat_input triggered it)
3. Section 6.2 displays the greeting
4. Section 6.3 captures "Hello", adds it to history, displays it
5. Section 6.4 will generate and display the AI response (next section)
6. On the next rerun, Section 6.2 will display: greeting → "Hello" → AI response

**📝 Action:** Uncomment Section 6.3 in the `.py` file. Try typing a message - you should see it appear in the chat!

---

## Section 6.4: Generate and display a response

Finally, we need to generate a response and display it. For this primer, we'll use a simple echo response. In the **chatbot activity**, you'll learn to connect this to OpenAI's API for real AI responses.

```python
# For now, create a simple echo response
# (In the chatbot activity, you'll replace this with OpenAI API calls)
response = f"You said: {prompt}"

# Display the response
st.chat_message("assistant").write(response)

# Add assistant response to history
st.session_state.messages.append({"role": "assistant", "content": response})
```

**Step-by-step breakdown:**

1. **Create response:** For now, we just echo back what the user said
2. **Display immediately:** Show it in an assistant chat bubble
3. **Save to history:** Add it to `st.session_state.messages` so it persists

**The complete flow:**
1. User types "Hello" → Section 6.3 captures it and adds to history
2. Section 6.4 runs
3. Creates response: "You said: Hello"
4. Displays it in assistant chat bubble
5. Adds response to history
6. On next rerun, Section 6.2 displays entire conversation

**What you'll learn in the chatbot activity:**
- How to connect to OpenAI's API
- How to stream responses token-by-token (word-by-word)
- How to pass conversation history for context
- How to handle API errors gracefully

For now, this simple echo demonstrates the complete chatbot pattern!

📝 **Action:** Uncomment **Section 6.4** in the `.py` file.

---

## How it all works together (what you just built)

If you zoom out, here's what your app is doing:

**User opens the app (first run):**
```
1. Script runs from top to bottom
2. Section 6.1: Initialize messages with greeting
3. Section 6.2: Loop displays the greeting message
4. Section 6.3: Chat input appears (no message yet)
5. Section 6.4: Skipped (no new user message)
6. Page shows: greeting message + input box at bottom
```

**User types "Hello" and presses Enter:**
```
1. Chat input triggers a rerun
2. Section 6.1: messages exists → Skip initialization
3. Section 6.2: Loop displays the greeting
4. Section 6.3: Captures "Hello"
   - Appends to messages: [greeting, user:"Hello"]
   - Displays "Hello" in a user bubble
5. Section 6.4: Generates response
   - Creates echo response: "You said: Hello"
   - Displays it in assistant bubble
   - Appends to messages
6. Rerun happens
7. Section 6.2 displays all messages: greeting + "Hello" + "You said: Hello"
```

**The pattern continues forever:**
- Every new message added to history
- Display always shows complete history
- Session state keeps everything persistent
- In the chatbot activity, you'll add real AI that uses this history for conversation context

That's the essential Streamlit chatbot pattern!

---

# Part 7: Additional components (optional)

These are useful tools you'll see in many Streamlit apps.

---

## Section 7.1: Spinners and `st.stop()`

- `st.spinner(...)` shows "working…" while code runs
- `st.stop()` ends the current run early (useful for "must upload first" patterns)

```python
with st.spinner("Processing..."):
    time.sleep(2)  # Simulate work
st.success("Done!")

# Stop execution if condition not met
if not uploaded_file:
    st.warning("Upload a file to continue below.")
    st.stop()
```

📝 **Action:** Uncomment **Section 7.1** in the `.py` file.

---

## Section 7.2: Dynamic updates with `st.empty()`

`st.empty()` creates a placeholder you can update:

```python
placeholder = st.empty()

placeholder.info("Step 1/5...")
time.sleep(0.5)

placeholder.info("Step 2/5...")
time.sleep(0.5)

placeholder.success("All steps complete!")
```

Without `st.empty()`, all messages would stack up. With it, each update replaces the previous one.

📝 **Action:** Uncomment **Section 7.2** in the `.py` file.

---

## Section 7.3: Display helpers

- `st.json(...)` for structured output
- `st.code(...)` for code snippets

```python
st.json({"status": "ok", "items": [1, 2, 3]})
st.code("print('Hello from code block')", language="python")
```

📝 **Action:** Uncomment **Section 7.3** in the `.py` file.

---

## Section 7.4: Download button

`st.download_button(...)` lets users download generated content.

```python
import json

content = json.dumps({"message": "Thanks for learning Streamlit!"}, indent=2)
st.download_button("Download JSON", data=content, file_name="example.json", mime="application/json")
```

📝 **Action:** Uncomment **Section 7.4** in the `.py` file.

---

# Summary: Core concepts

If you can recall and explain these four sentences, you're in great shape:

1. Streamlit runs a Python script and turns it into a web app.
2. Every user interaction reruns the script top-to-bottom.
3. Widgets return values from the browser into your Python variables.
4. `st.session_state` is how you persist data across reruns.

**You're ready to build AI applications with Streamlit!** 🚀
