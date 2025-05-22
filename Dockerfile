# 1. Imagem base
FROM python:3.12-slim

# 2. Instalar dependências do sistema
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 3. Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# 4. Adicionar Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"

# 5. Desativar o venv do Poetry
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# 6. Criar diretório de trabalho
WORKDIR /desafio

# 7. Copiar arquivos do projeto
COPY pyproject.toml poetry.lock ./
COPY . .

# 8. Instalar dependências com Poetry
RUN poetry install

# 9. Comando para iniciar o servidor FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
