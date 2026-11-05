import numpy as np
from openai import OpenAI
client= OpenAI(base_url="http://localhost:11434/v1",
    api_key="ollama")

def cosine_similarity(vector1, vector2):

    v1 = np.array(vector1)
    v2 = np.array(vector2)

    return np.dot(v1, v2) / (
        np.linalg.norm(v1) *
        np.linalg.norm(v2)
    )

def create_embedding(content):
    embedding=client.embeddings.create(
    model='nomic-embed-text:latest',input=content).data[0].embedding
    return embedding