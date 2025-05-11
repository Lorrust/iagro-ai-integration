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

    messages = [{"role": "system", "content": system_prompt.strip()}]

    # TODO: Evaluate chroma context efficiency and relevance
    if chroma_results:
        documents = chroma_results.get('documents', [[]])[0]
        context = "\n\n".join(documents)
        messages.append({"role": "system", "content": f"Contexto adicional:\n\n{context}"})

    if request.message_history:
        for msg in request.message_history:
            messages.append({"role": msg.role, "content": msg.content})

    user_content = build_user_content(request)
    messages.append({"role": "user", "content": user_content})

    logger.debug("[OpenAI] Sending request with following messages:")
    for i, msg in enumerate(messages):
        logger.debug("[OpenAI] message {}:\nrole: {}\ncontent:\n{}\n", i + 1, msg["role"], msg["content"])


    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
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
