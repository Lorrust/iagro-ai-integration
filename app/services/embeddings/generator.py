from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_text_embeddings(text: str):
    """
    Generates embeddings for the given text using a pre-trained model.

    Args:
        text (str): The text to generate embeddings for.

    Returns:
        Tensor: The generated data structure of embeddings.
    """
    embedding = model.encode(text)
    return embedding
