from openai import OpenAI

from similarity import cosine_similarity

client= OpenAI(base_url="http://localhost:11434/v1",
    api_key="ollama")

embedding_1 =client.embeddings.create(
    model='nomic-embed-text:latest',
    input=input("enter the 1st input:")
).data[0].embedding

embedding_2=client.embeddings.create(
    model='nomic-embed-text:latest',
    input=input("enter the 2nd input:")
).data[0].embedding

# print(type(embedding_1))
# print(len(embedding_1))

# print(type(embedding_2))
# print(len(embedding_2))
# # print(embedding)
score = cosine_similarity(embedding_1, embedding_2)

print(score)
