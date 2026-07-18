
import requests
import math


def get_embedding(text):
    """
    Calls Ollama's embedding endpoint for a single piece of text.
    Returns a list of floats (the embedding vector).
    """
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )
    if response.status_code != 200:
        raise Exception(f"Embedding error: {response.text}")

    data = response.json()
    return data["embedding"]