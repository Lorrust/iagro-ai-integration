import os
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI
from loguru import logger
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chroma.chroma_service import ChromaService
from app.constants import prompts, defaults

load_dotenv()

logger.add("logs/chat.log", rotation="1 MB", level="DEBUG", backtrace=True, diagnose=True)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma_service = ChromaService()

def build_user_content(request: ChatRequest):
    """
    Build the user content for the OpenAI model request.

    Args:
        request (ChatRequest): The request containing the message and optional image URL.

    Returns:
        list[dict[str, str]]: A list of dictionaries representing the user content.
    """
    content = [{"type": "text", "text": request.message}]
    if request.image_url:
        content.append({"type": "image_url", "image_url": {"url": str(request.image_url)}})
    return content

async def ask_ai(request: ChatRequest, chroma_results = None) -> ChatResponse:
    """
    Send the request to the OpenAI model, including the results from ChromaDB, if provided.

    Args:
        request (ChatRequest): The request containing the message and optional image URL.
        chroma_results (Optional): The results from ChromaDB to include in the prompt.

    Returns:
        ChatResponse: The AI's response containing the diagnosis.
    """
    system_prompt = prompts.DIAGNOSIS_SYSTEM_PROMPT

    if chroma_results:
        documents = chroma_results.get('documents', [[]])[0]
        context = "\n\n".join(documents)
        system_prompt += f"\nContexto encontrado pelo banco vetorial para auxiliar no seu diagnóstico:\n\n{context}"

    logger.debug(f"[ChromaDB] Context found:\n{chroma_results}")
    logger.debug(f"[OpenAI] Final prompt:\n{system_prompt.strip()}")

    logger.debug("Sending prompt to the model...")

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": build_user_content(request)}
            ],
            temperature=0.5
        )

        content = response.choices[0].message.content
        logger.debug(f"[OpenAI] Raw response:\n{content}")

        try:
            return ChatResponse(**json.loads(content))
        except json.JSONDecodeError as e:
            logger.error(f"Error decodifying JSON: {e}")
            logger.error(f"Content received:\n{content}")

            logger.warning("Response is not a valid JSON, using default fallback.")
            return ChatResponse(**defaults.FALLBACK_RESPONSE)

    except Exception as e:
        logger.exception(f"[OpenAI] Error processing response: {str(e)}")
        raise RuntimeError(f"Erro ao processar resposta da IA: {str(e)}")
