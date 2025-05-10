# TODO: Verify if this utility is still needed, since gpt-4o can handle image URLs directly.

import requests
import base64

def image_url_to_base64(image_url: str) -> str:
    response = requests.get(image_url)
    if response.status_code == 200:
        return base64.b64encode(response.content).decode('utf-8')
    else:
        raise Exception(f"Erro ao baixar a imagem: {response.status_code}")
