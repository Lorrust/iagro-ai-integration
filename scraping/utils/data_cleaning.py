import re

def clean_text(text: str, preserve_paragraphs: bool = True) -> str:
    """
    Cleans the input text by removing unnecessary characters and fixing spacing issues.

    Args:
        text (str): The input text to be cleaned.
        preserve_paragraphs (bool, optional): If True, keeps paragraph breaks; 
            otherwise, merges everything into a single line. Defaults to True.

    Returns:
        str: The cleaned text.
    """
    if not text:
        return ""

    # Remove carriage returns
    text = text.replace('\r', '')

    if preserve_paragraphs:
        # Replace multiple newlines (\n\n+) with a single paragraph break
        text = re.sub(r'\n\s*\n+', '\n\n', text)
        # Replace single newlines inside paragraphs with spaces
        text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    else:
        # Replace all newlines with spaces
        text = text.replace('\n', ' ')

    # Remove multiple spaces
    text = re.sub(r'[ \t]+', ' ', text)

    # Remove multiple spaces, tabs, or any other invisible characters
    text = re.sub(r'\s+', ' ', text)

    # Strip leading and trailing spaces
    text = text.strip()

    return text
