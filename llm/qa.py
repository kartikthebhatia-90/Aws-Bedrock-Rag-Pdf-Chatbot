import os
import boto3
from dotenv import load_dotenv

from retrieval.search import search
from llm.prompts import build_qa_prompt

load_dotenv()


def build_context(results):
    context_parts = []

    for r in results:
        context_parts.append(
            f"[Source: {r['source_file']} | Page: {r['page_number']}]\n{r['text']}"
        )

    return "\n\n".join(context_parts)


def build_sources(results):
    lines = []
    seen = set()

    for r in results:
        key = (r["source_file"], r["page_number"])
        if key not in seen:
            seen.add(key)
            lines.append(f"- {r['source_file']} (Page {r['page_number']})")

    return "\n".join(lines)


def generate_answer(prompt: str) -> str:
    region = os.getenv("AWS_REGION", "ap-southeast-2")
    api_key = os.getenv("AWS_BEARER_TOKEN_BEDROCK")
    model_id = os.getenv("BEDROCK_MODEL_ID")

    if not api_key:
        raise ValueError("AWS_BEARER_TOKEN_BEDROCK is missing in .env")

    if not model_id:
        raise ValueError("BEDROCK_MODEL_ID is missing in .env")

    os.environ["AWS_BEARER_TOKEN_BEDROCK"] = api_key

    client = boto3.client(
        service_name="bedrock-runtime",
        region_name=region,
    )

    response = client.converse(
        modelId=model_id,
        messages=[
            {
                "role": "user",
                "content": [{"text": prompt}],
            }
        ],
        inferenceConfig={
            "maxTokens": 500,
            "temperature": 0.2,
        },
    )

    return response["output"]["message"]["content"][0]["text"]


def answer_question(question: str, top_k: int = 5):
    results = search(question, top_k=top_k)
    context = build_context(results)
    prompt = build_qa_prompt(question, context)
    answer = generate_answer(prompt)
    sources = build_sources(results)

    print("\n" + "=" * 80)
    print("FINAL ANSWER:\n")
    print(answer)

    print("\nSOURCES USED:")
    print(sources)
    print("=" * 80)


def main():
    question = input("Enter your question: ").strip()

    if not question:
        print("Question cannot be empty.")
        return

    answer_question(question)


if __name__ == "__main__":
    main()