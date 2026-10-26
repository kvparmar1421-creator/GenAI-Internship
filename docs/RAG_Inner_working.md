# Inner Structure of RAG in Simple English

**RAG stands for Retrieval-Augmented Generation.**

RAG is an AI technique that helps an AI answer questions using
information stored in documents, PDFs, text files, or a database such as
ChromaDB.

## 1. Inner Architecture of RAG

``` text
DOCUMENTS / DATA
(PDFs, text files, company documents)
          |
          v
       CHUNKING
(Split documents into small text pieces)
          |
          v
    EMBEDDING MODEL
(Convert text into numerical vectors)
          |
          v
   VECTOR DATABASE
       (ChromaDB)
          |
          |   User asks a question
          v
    USER QUERY + EMBEDDING
(Convert the question into a vector)
          |
          v
       RETRIEVAL
(Find the most relevant text pieces)
          |
          v
   PROMPT CONSTRUCTION
(Combine question + retrieved information)
          |
          v
          LLM
(Uses the context to generate an answer)
          |
          v
      FINAL ANSWER
```

## 2. Explanation of Each Component

  Component             Simple meaning
  --------------------- ------------------------------------------------
  Documents             The information we want AI to use
  Chunking              Dividing large text into smaller pieces
  Embedding model       Converting text into numerical representations
  ChromaDB              Storing and searching text vectors
  User query            The question asked by the user
  Retrieval             Finding relevant information
  Prompt construction   Giving the question and information to the AI
  LLM                   The AI model that generates an answer
  Final answer          The response shown to the user

## 3. Real-Life Example

Suppose you build a company-policy chatbot.

-   **Document:** The company provides 12 paid leaves per year.
-   **Chunking:** The policy is divided into smaller text sections.
-   **Embedding:** Each section is converted into a vector.
-   **ChromaDB:** Stores the sections and their vectors.
-   **User question:** "How many paid leaves can I take?"
-   **Retrieval:** Finds the section about paid leaves.
-   **LLM:** Uses the retrieved policy to formulate a response.
-   **Final answer:** "According to the company policy, employees
    receive 12 paid leaves per year."

## 4. Main Stages of RAG

### Stage 1: Indexing

**Documents → Chunking → Embeddings → Vector Database**

This stage prepares and stores information so it can be searched later.

### Stage 2: Question Answering

**User Question → Retrieval → Context + Question → LLM → Answer**

This stage finds relevant information and uses it to answer the user's
question.

## 5. Remember

-   **Embedding model:** Helps represent text numerically for semantic
    search.
-   **ChromaDB:** Stores and searches information using vectors.
-   **Retriever:** Finds the most relevant text pieces.
-   **LLM:** Generates the final answer using the retrieved context.

**In short:** RAG retrieves relevant information first, then uses an AI
model to generate an answer grounded in that information.
