#!/bin/bash

echo "Ativando ambiente virtual com Poetry..."
poetry shell

echo "Instalando dependências com Poetry..."
poetry install

echo "Iniciando a aplicação..."
poetry run uvicorn app.main:app --reload
