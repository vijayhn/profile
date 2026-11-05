from retriever import load_documents
from similarity import cosine_similarity,create_embedding
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load configuration
load_dotenv()

# Create AI client
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

documents= load_documents()

document_embeddings={}
for filename,content in documents.items():
    document_embeddings[filename]= create_embedding(content)


print("=" * 40)
print("    My RAG Assistant - Basic")
print("=" * 40)

while True:

    user_input = input("\nYou : ")

    if user_input.lower() == "quit":
        print("\nAI  : Goodbye! Have a great day.")
        break

    question_embedding= create_embedding(user_input)

    best_score=-1
    best_document=None
    for filename,doc_embedding in document_embeddings.items():
        score=cosine_similarity(question_embedding,doc_embedding)

        if score>best_score:
            best_score=score
            best_document=filename

    context = documents[best_document]

    prompt=f"""
        Answer the question only using the following information. 

        Context: {context}

        Question: {user_input}
        """

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("\nAI :", response.choices[0].message.content)

