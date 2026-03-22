QA_SYSTEM_PROMPT = """
You are a helpful assistant for construction and safety documents.
Answer only from the provided context.
If the answer is not in the context, say that clearly.
Be concise, clear, and factual.
""".strip()


def build_qa_prompt(question: str, context: str) -> str:
    return f"""
Context:
{context}

Question:
{question}

Instructions:
- Answer using only the context above.
- If the context is insufficient, say so.
- Give a clear and professional response.

Answer:
""".strip()


SUMMARY_PROMPT = """
Summarise the following text into a formal business-style summary.
Focus on the main points, decisions, risks, and outcomes.
""".strip()


SENTIMENT_PROMPT = """
Classify the sentiment of the following text as Positive, Neutral, or Negative.
Then explain briefly why.
""".strip()