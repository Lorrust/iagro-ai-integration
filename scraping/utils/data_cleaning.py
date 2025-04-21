# Removes not needed characters from the text generated in docling converter files and scraping
def clean_text(text: str, preserve_paragraphs=True):
    
    """
    Cleans the input text by removing or replacing newline characters.

    Args:
        text (str): The input text to be cleaned.
        preserve_paragraphs (bool, optional): If True, replaces newline characters ('\n') 
            with a space or another delimiter. If False, removes all newline and carriage 
            return characters ('\n' and '\r'). Defaults to False.

    Returns:
        str: The cleaned text with newline characters handled based on the 
        `preserve_paragraphs` parameter.
    """

    if preserve_paragraphs:
        
        cleaned_text = text.replace('\n', ' ')
    else:
        
        cleaned_text = text.replace('\n', ' ').replace('\r', '')
    
    return cleaned_text