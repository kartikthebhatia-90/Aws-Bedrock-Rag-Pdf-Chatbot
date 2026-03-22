import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import streamlit as st

from retrieval.search import search
from llm.qa import build_context, build_sources, generate_answer
from llm.prompts import build_qa_prompt


st.set_page_config(page_title="Construction RAG Chatbot", layout="wide")

st.title("Construction RAG Chatbot")
st.write("Ask questions from your uploaded construction and safety PDFs.")

question = st.text_input("Enter your question")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Retrieving relevant chunks..."):
            results = search(question, top_k=5)
            context = build_context(results)
            prompt = build_qa_prompt(question, context)

        with st.spinner("Generating answer with Bedrock..."):
            answer = generate_answer(prompt)

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Sources Used")
        st.text(build_sources(results))

        st.subheader("Retrieved Chunks")
        for r in results:
            with st.expander(
                f"{r['source_file']} | Page {r['page_number']} | Rank {r['rank']}"
            ):
                st.write(r["text"])