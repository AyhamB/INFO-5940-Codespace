# Retrieval-Augmented Generation (RAG)

**INFO 5940 · Assignment 2**

Open [workbook.ipynb](workbook.ipynb) to work through the RAG examples from class.
You will start by retrieving passages from a text document, then use SQL to
retrieve information from a structured database. In both parts, you will examine
what information reaches the model and whether it supports the answer.

## Part 1: RAG with a vector database

Sections A through J cover document retrieval:

- Load the source document and split it into chunks.
- Create embeddings and search for related text with Chroma.
- Retrieve passages and include them in a model request.
- Compare answers with the retrieved evidence.
- Use a model to help choose chunk boundaries and compare the results.

## Part 2: RAG with a structured database

Sections K through P use the [Chinook](https://github.com/lerocha/chinook-database)
sample music-store database:

- Inspect the tables and run a SQL query.
- Give a model the schema and ask it to generate SQL.
- Execute the query and use its results as context for an answer.
- Check the query, resolve ambiguous questions, and identify conclusions the
  records cannot support.

## Working through the notebook

Save, commit, and push any pending work before updating. Then update your fork
using **Sync fork → Update branch** on GitHub. In your
Codespace terminal, on `main`, pull the updates:

```bash
git pull --no-rebase --no-edit origin main
```

Then open the Command Palette and select **Codespaces: Rebuild Container**.
Wait for setup to finish. The rebuild installs the packages from the updated
`requirements.txt`; no separate installation command is needed.

Run the cells in order and complete the six **Your observations** response areas.
A few sentences for each is enough. Refer to your actual results and keep the
code outputs visible. Canvas provides the setup and submission instructions.

## Files

| File | Purpose |
| --- | --- |
| [workbook.ipynb](workbook.ipynb) | Both parts of the assignment, with explanations and six response areas. Complete your work here. |
| [data/RAG_source.txt](data/RAG_source.txt) | Source document for vector retrieval. |

The SQL sections also use `data/Chinook.db`, which is already included in the
repository from the earlier classroom example. Only edit `workbook.ipynb`;
keep the supplied data files unchanged.

## Saving and submitting

Save your code, relevant outputs, and written responses in `workbook.ipynb`.
Follow the [course README](../../README.md#saving-and-submitting-your-work) to
commit and push your work. Submit the link requested on Canvas.
