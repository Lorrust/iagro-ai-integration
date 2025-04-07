# IAgro AI Integration

Este módulo faz parte do projeto [IAgro](https://github.com/Lorrust/iagro).

## Descrição do Módulo

API desenvolvida em Python com FastAPI, responsável por:

- Receber mensagens e imagens dos usuários.
- Enviar a consulta para a API da OpenAI.
- Usar RAG com ChromaDB para aprimorar as respostas com conhecimento específico.
- Retornar o diagnóstico, categoria e tipo do problema identificado.

## Instruções

### 1. Clone o Repositório

```bash
git clone https://github.com/Lorrust/ai-integration.git
cd ia-integration
```

### Execução

```ps
.\start.ps1
```

## Variáveis de Ambiente

Crie um arquivo .env na raiz com o seguinte conteúdo:

```sh
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Rodando a API

Com o ambiente ativado:

```bash
uvicorn app.main:app --reload
```

A API estará disponível em: http://localhost:8000

Caso deseje visulizar a documentação, insira `/docs` ao final do link acima.

## Tecnologias Utilizadas

- Python 3.13
- FastAPI
- ChromaDB
- OpenAI (ChatGPT API)
- dotenv
