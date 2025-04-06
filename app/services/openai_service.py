import os
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI
from loguru import logger
from app.schemas.chat import ChatRequest, ChatResponse

load_dotenv()

logger.add("logs/chat.log", rotation="1 MB", level="DEBUG", backtrace=True, diagnose=True)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def ask_ai(request: ChatRequest) -> ChatResponse:
    system_prompt = """
Você é um assistente agrícola especializado em culturas de arroz.
Seu objetivo é analisar descrições de problemas enviadas por produtores e retornar um diagnóstico estruturado em JSON.

Retorne o diagnóstico no seguinte formato JSON, e **somente o JSON**:
{
  "categoria": "Doença | Praga | Deficiência Nutricional | Outro",
  "tipo": "Nome do problema",
  "descricao": "Explicação curta do que é o problema",
  "recomendacao": "Ação recomendada, tratamento ou medida preventiva"
}

Sempre que identificar o problema, traga o nome científico e o nome popular, se possível.

IMPORTANTE: Sempre responda SOMENTE no formato JSON fornecido.
Se não conseguir identificar o problema, use o seguinte formato:
{
  "categoria": "Outro",
  "tipo": "Não identificado",
  "descricao": "Não foi possível identificar o problema com base na imagem ou descrição fornecida.",
  "recomendacao": "Recomenda-se procurar um agrônomo especializado ou enviar uma imagem mais clara e detalhada."
}

NUNCA responda com mensagens de erro, nem explique. Sempre retorne um JSON, mesmo que as informações estejam incompletas.
"""

    user_content = [
        {"type": "text", "text": request.message}
    ]

    if request.image_url:
        user_content.append({
            "type": "image_url",
            "image_url": {"url": str(request.image_url)}
        })

    logger.debug("Enviando prompt para o modelo...")

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_content}
            ],
            temperature=0.5
        )

        content = response.choices[0].message.content
        logger.debug(f"Resposta bruta da IA:\n{content}")

        try:
            parsed = json.loads(content)
            logger.debug(f"Resposta JSON parseada:\n{parsed}")
            return ChatResponse(**parsed)
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON: {e}")
            logger.error(f"Conteúdo recebido:\n{content}")

            fallback = {
                "categoria": "Outro",
                "tipo": "Não identificado",
                "descricao": "Não foi possível identificar o problema com base na imagem ou descrição fornecida.",
                "recomendacao": "Recomenda-se procurar um agrônomo especializado ou enviar uma imagem mais clara e detalhada."
            }

            logger.warning("Utilizando fallback padrão.")
            return ChatResponse(**fallback)

    except Exception as e:
        logger.exception(f"Erro inesperado ao processar a resposta da IA: {str(e)}")
        raise RuntimeError(f"Erro ao processar a resposta da IA: {str(e)}")
