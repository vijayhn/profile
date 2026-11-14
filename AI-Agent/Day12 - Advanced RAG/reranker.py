from openai import OpenAI
import os 
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


MODEL = os.getenv("MODEL", "qwen2.5-coder:14b")


def rerank(
    query,
    candidates,
    top_k=3
):

    scored = []

    for candidate in candidates:

        prompt = f"""
You are a document relevance evaluator.

User Query:
{query}

Document:
{candidate["text"]}

Give a relevance score from 0 to 100.

100 = directly answers the query
0 = completely irrelevant

Return ONLY the number.
"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        score_text = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        try:
            score = float(score_text)
        except ValueError:
            score = 0

        scored.append({
            **candidate,
            "rerank_score": score
        })

    scored.sort(
        key=lambda item:
        item["rerank_score"],
        reverse=True
    )

    return scored[:top_k]


