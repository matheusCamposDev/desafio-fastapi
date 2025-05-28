# Tecnologias

- Potry `version 2.1.2`
- Docker `version 28.1.1`
- Docker-compose `version 2.35.1`
- Pytest `version 8.3.5`
- Python `version >=3.11`
- Fastapi `version 0.115.12`
- Pyjwt `version 2.10.1`
- Psycopg2-binary `version 2.9.10`

# Como usar

### Online
Você pode acessar a versão online disponível no Render através do link: https://desafio-fastapi.onrender.com/docs#/

    OBS: Ao acessar possa ser que a aplicação não aparece como disponível na hora, isso porque a hospedagem no Render desabilita o servidor depois de 15 minutos de inatividade quando não há requisições aos endpoints a aplicação, retornando ao normal quando houver uma nova solicitação depois de 35 segundos.

### Clonando e executando com docker localmente

1. Clone o repositório: `https://github.com/matheusCamposDev?tab=repositories`

2. Crie um arquivo `.env` na mesma pasta do app e configure as variáveis de ambiente:

Exemplo:
    
        POSTGRES_USER= root
        POSTGRES_PASSWORD= root
        POSTGRES_DB= desafiodb
        DATABASE_URL = "postgresql://root:root@localhost:5432/desafiodb" 
        REFRESH_TOKEN_SECRET = "secret-token"
        TOKEN_EXPIRES = 15
        REFRESH_TOKEN_EXPIRES = 7
        ALGORITHM = "HS256"

4. Tenha o docker e docker compose instalado na sua máquina e excute o comando: `docker compose up --build`

5. Acesse a aplicação através do container pelo link:

        Linux: `http://0.0.0.0:8000/docs`
        
        Windows: `http://localhost:8000/docs`
