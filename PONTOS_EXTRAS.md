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
- `SUPABASE_RENDER.md`
- `PYTHONANYWHERE_DEPLOY.md`
- `requirements.txt` com `gunicorn` e `whitenoise`
- `caronas/settings.py` com suporte a variaveis de ambiente

O projeto foi publicado no Render usando Blueprint com `plan: free`. O projeto tambem suporta `DATABASE_URL` para conectar o Render a um Postgres externo, como Supabase.

O Postgres do ponto extra foi comprovado no ambiente Docker local. Para usar Postgres tambem em producao, configure Supabase conforme [SUPABASE_RENDER.md](SUPABASE_RENDER.md).

URL publica:

```text
https://sistema-agendamento-caronas.onrender.com
```

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

## Validacao em Producao

Aplicacao publicada no Render:

```text
https://sistema-agendamento-caronas.onrender.com
```

Validacao externa:

```text
HTTP 200
https://sistema-agendamento-caronas.onrender.com/contas/login/?next=/
```

O deploy aparece como **live** no painel do Render.
