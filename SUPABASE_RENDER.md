# Usar Supabase como Postgres em Producao

Este guia conecta a aplicacao publicada no Render a um banco Postgres gratuito do Supabase.

Arquitetura:

```text
Render Free Web Service -> Django
Supabase Free Project -> Postgres
```

## 1. Criar projeto no Supabase

1. Acesse `https://supabase.com`.
2. Crie uma conta ou entre com GitHub.
3. Crie um novo projeto.
4. Guarde a senha do banco definida na criacao do projeto.

## 2. Copiar a connection string

No projeto do Supabase:

1. Clique em **Connect**.
2. Escolha **Session pooler**.
3. Copie a connection string.

Use **Session pooler**, porque o Render geralmente usa rede IPv4 e o pooler do Supabase atende esse caso melhor que a conexao direta.

O formato sera parecido com:

```text
postgresql://postgres.PROJECT_REF:SENHA@aws-REGIAO.pooler.supabase.com:5432/postgres?sslmode=require
```

Se nao vier com `?sslmode=require`, adicione no final.

## 3. Configurar no Render

No servico `sistema-agendamento-caronas` no Render:

1. Va em **Environment**.
2. Adicione a variavel:

```text
DATABASE_URL=postgresql://postgres.PROJECT_REF:SENHA@aws-REGIAO.pooler.supabase.com:5432/postgres?sslmode=require
```

3. Clique em **Save Changes**.
4. Faca um novo deploy manual.

## 4. Conferir o deploy

No log do Render, devem aparecer:

```text
python manage.py migrate --noinput
python manage.py criar_dados_demo
gunicorn caronas.wsgi:application
```

Depois acesse:

```text
https://sistema-agendamento-caronas.onrender.com
```

## 5. Como explicar na apresentacao

Use esta frase:

```text
A aplicacao esta publicada no Render e usa Postgres em producao via Supabase. Localmente, Docker Compose tambem sobe um Postgres para desenvolvimento e validacao.
```

## Observacao

Se a URL tiver caracteres especiais na senha, copie a connection string diretamente do Supabase para evitar erro de autenticacao.
