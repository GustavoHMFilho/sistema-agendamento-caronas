# Pontos Extras

Este arquivo resume como o projeto atende aos itens extras do enunciado.

## Docker

Arquivos relacionados:

- `Dockerfile`
- `docker-compose.yml`
- `.dockerignore`
- `docker/entrypoint.sh`

Comando para executar:

```bash
cp .env.example .env
docker compose up --build
```

No Windows PowerShell:

```powershell
copy .env.example .env
docker compose up --build
```

## Postgres

O `docker-compose.yml` possui um servico `db` com a imagem oficial `postgres:16-alpine`.

Quando as variaveis `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST` e `POSTGRES_PORT` existem, o Django usa Postgres em vez de SQLite.

O workflow `.github/workflows/django-postgres.yml` tambem executa os testes com um servico Postgres real no GitHub Actions.

## Producao

Arquivos relacionados:

- `render.yaml`
- `PYTHONANYWHERE_DEPLOY.md`
- `requirements.txt` com `gunicorn` e `whitenoise`
- `caronas/settings.py` com suporte a variaveis de ambiente

O projeto esta preparado para deploy gratuito no Render usando Blueprint com `plan: free` e SQLite. O Postgres do ponto extra foi comprovado no ambiente Docker local.

Caso o Render ainda solicite informacoes de pagamento, use o deploy gratuito no PythonAnywhere descrito em `PYTHONANYWHERE_DEPLOY.md`.

Para concluir o ponto extra de producao, publique o repositorio em um servico como Render, Railway, Fly.io ou VPS e entregue a URL publica gerada.

## Evidencias sugeridas para apresentar

- Mostrar o arquivo `docker-compose.yml`.
- Executar `docker compose up --build` em uma maquina com Docker.
- Mostrar o Postgres no `docker-compose.yml`.
- Abrir o GitHub Actions e mostrar o workflow `Django Postgres CI` passando.
- Se publicado, abrir a URL publica da aplicacao.

## Validacao Local Realizada

Validacao feita em ambiente local com Docker Desktop:

```text
docker compose up --build -d
```

Resultado observado:

- Container `trabalhodjango-db-1` com Postgres ativo na porta `5432`.
- Container `trabalhodjango-web-1` ativo na porta `8000`.
- Migrations executadas automaticamente no banco Postgres.
- Arquivos estaticos coletados automaticamente.
- Dados de demonstracao criados automaticamente.
- Login em `http://127.0.0.1:8000/contas/login/` respondeu HTTP `200`.

Validacoes executadas dentro do container:

```text
docker compose exec -T web python manage.py check
System check identified no issues (0 silenced).

docker compose exec -T web python manage.py test
Ran 5 tests in 4.364s
OK
```
