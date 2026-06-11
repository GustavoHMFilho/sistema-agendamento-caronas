# Sistema de Agendamento de Caronas

Projeto desenvolvido com Django para a disciplina **GAC116 - Programacao Web**.

## Sobre o Projeto

O sistema permite o gerenciamento de caronas entre usuarios, possibilitando:

- Cadastro de usuarios e perfis.
- Cadastro de veiculos.
- Cadastro de locais de origem e destino.
- Oferta de caronas.
- Busca e listagem de caronas disponiveis.
- Reserva e cancelamento de vagas por passageiros.
- Avaliacao das viagens realizadas.

## Funcionalidades

- Ambiente administrativo protegido por login e senha.
- Admin personalizado com Jazzmin.
- Ambiente do usuario protegido por login e senha.
- Interface responsiva com Bootstrap.
- Modelagem com banco relacional SQLite ou Postgres.
- Validacoes de negocio nos modelos.
- Testes automatizados para fluxos principais.

## Checkpoint 1

Entrega focada na modelagem completa do sistema e na configuracao do ambiente administrativo do Django.

Recursos configurados no Django Admin:

- Integracao com Jazzmin para personalizacao visual do Django Admin.
- `list_display` para exibicao dos principais campos das entidades.
- `list_filter` para filtros rapidos de registros.
- `search_fields` para busca de usuarios, rotas, placas e locais.
- `inlines` para cadastro relacionado:
  - veiculos dentro do perfil do usuario;
  - reservas dentro da carona;
  - avaliacoes dentro da reserva.
- Validacoes com `clean()` nos modelos:
  - impedimento de cadastro de caronas no passado;
  - origem e destino diferentes;
  - bloqueio do motorista reservar a propria carona;
  - controle do limite maximo de vagas.

## Checkpoint 2

A entrega completa inclui a area do usuario com login, telas responsivas com Bootstrap e fluxo funcional para oferecer caronas, reservar vagas, consultar reservas, cadastrar veiculos, cadastrar locais e avaliar viagens.

## Modelagem

Entidades principais:

- `PerfilUsuario`: dados complementares do usuario autenticavel.
- `Veiculo`: veiculos vinculados aos motoristas.
- `Local`: pontos de origem e destino.
- `Carona`: oferta de viagem com motorista, veiculo, rota, horario, valor e vagas.
- `Reserva`: solicitacao ou confirmacao de vaga por passageiros.
- `Avaliacao`: nota e comentario associados a reserva.

O diagrama entidade-relacionamento esta disponivel em [MODELAGEM_ER.md](MODELAGEM_ER.md).

## Tecnologias Utilizadas

- Python.
- Django.
- SQLite.
- Postgres.
- Jazzmin.
- Bootstrap.
- Docker.
- Gunicorn.
- WhiteNoise.

## Pontos Extras

O projeto cumpre os seguintes pontos extras:

- Conteinerizacao com Docker: `Dockerfile` e `docker-compose.yml`.
- Integracao com Postgres: servico `db` no Docker Compose usando a imagem oficial do Postgres, validado localmente.
- Aplicacao em producao: publicada no Render em `https://sistema-agendamento-caronas.onrender.com`.

O deploy em producao usa `gunicorn`, `whitenoise`, variaveis de ambiente e `render.yaml` com plano gratuito.

Mais detalhes e evidencias de validacao estao em [PONTOS_EXTRAS.md](PONTOS_EXTRAS.md).

## Como Executar o Projeto

### 1. Clonar o repositorio

```bash
git clone https://github.com/GustavoHMFilho/sistema-agendamento-caronas
```

### 2. Entrar na pasta do projeto

```bash
cd sistema-agendamento-caronas
```

### 3. Criar o ambiente virtual

Windows:

```bash
python -m venv .venv
```

Linux/macOS:

```bash
python3 -m venv .venv
```

### 4. Ativar o ambiente virtual

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 5. Instalar as dependencias

```bash
pip install -r requirements.txt
```

### 6. Executar as migracoes

```bash
python manage.py migrate
```

### 7. Criar dados de demonstracao

```bash
python manage.py criar_dados_demo
```

### 8. Iniciar o servidor

```bash
python manage.py runserver
```

Depois acesse:

- Area do usuario: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

## Usuarios de Demonstracao

| Perfil | Usuario | Senha |
| --- | --- | --- |
| Administrador | `admin` | `admin123` |
| Motorista | `motorista` | `teste123` |
| Passageiro | `passageiro` | `teste123` |

## Como Testar

1. Entre como `passageiro`.
2. Acesse a pagina de caronas disponiveis.
3. Abra os detalhes de uma carona e reserve uma vaga.
4. Confira a reserva em "Minhas reservas".
5. Entre como `motorista`.
6. Cadastre um veiculo, um local ou ofereca uma nova carona.
7. Entre no `/admin/` como `admin` para visualizar a modelagem, filtros, buscas, listas e inlines.

## Testes Automatizados

```bash
python manage.py test
```

## Executar com Docker e Postgres

### 1. Criar o arquivo de ambiente

Windows:

```bash
copy .env.example .env
```

Linux/macOS:

```bash
cp .env.example .env
```

### 2. Subir os containers

```bash
docker compose up --build
```

O container da aplicacao executa automaticamente:

- `python manage.py migrate --noinput`
- `python manage.py collectstatic --noinput`
- `python manage.py criar_dados_demo`

Depois acesse:

- Area do usuario: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

### 3. Parar os containers

```bash
docker compose down
```

### 4. Apagar tambem o banco Postgres local

Use apenas se quiser reiniciar os dados do zero:

```bash
docker compose down -v
```

## Deploy em Producao

A aplicacao esta publicada no Render:

```text
https://sistema-agendamento-caronas.onrender.com
```

O deploy foi feito por Blueprint usando o arquivo `render.yaml`.

Em producao, mantenha:

```text
DJANGO_DEBUG=False
```
