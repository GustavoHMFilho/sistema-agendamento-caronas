# Deploy Gratuito no PythonAnywhere

Este guia serve para publicar a aplicacao em producao sem informar cartao de credito.

O PythonAnywhere possui plano gratuito com uma aplicacao web publica em:

```text
seu-usuario.pythonanywhere.com
```

## 1. Criar conta gratuita

1. Acesse `https://www.pythonanywhere.com/pricing/`.
2. Escolha o plano gratuito **Beginner**.
3. Crie sua conta.

## 2. Abrir um Bash Console

No painel do PythonAnywhere:

1. Va em **Consoles**.
2. Abra um **Bash**.

## 3. Clonar o projeto

```bash
git clone https://github.com/GustavoHMFilho/sistema-agendamento-caronas.git
cd sistema-agendamento-caronas
```

## 4. Criar ambiente virtual

Escolha a versao de Python mais nova disponivel na sua conta.

Exemplo:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Se `python3.13` nao existir, tente:

```bash
python3.12 -m venv .venv
```

## 5. Preparar banco e arquivos estaticos

No plano gratuito, use SQLite para producao simples:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py criar_dados_demo
```

## 6. Criar Web App

1. Va em **Web**.
2. Clique em **Add a new web app**.
3. Escolha seu dominio gratuito `seu-usuario.pythonanywhere.com`.
4. Escolha **Manual configuration**.
5. Escolha a mesma versao de Python usada no ambiente virtual.

## 7. Configurar virtualenv

Na pagina **Web**, em **Virtualenv**, informe o caminho:

```text
/home/seu-usuario/sistema-agendamento-caronas/.venv
```

## 8. Configurar WSGI

Na pagina **Web**, clique no arquivo WSGI e substitua o conteudo pelo modelo abaixo, trocando `seu-usuario` pelo seu usuario do PythonAnywhere:

```python
import os
import sys

path = '/home/seu-usuario/sistema-agendamento-caronas'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'caronas.settings'
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_ALLOWED_HOSTS'] = '.pythonanywhere.com'
os.environ['DJANGO_SECRET_KEY'] = 'troque-esta-chave-em-producao'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 9. Configurar arquivos estaticos

Na pagina **Web**, em **Static files**, adicione:

```text
URL: /static/
Directory: /home/seu-usuario/sistema-agendamento-caronas/staticfiles
```

## 10. Recarregar a aplicacao

Clique em **Reload** na pagina **Web**.

Depois acesse:

```text
https://seu-usuario.pythonanywhere.com/
```

## Usuarios de demonstracao

```text
admin / admin123
motorista / teste123
passageiro / teste123
```

## Observacao

Docker e Postgres ja foram validados localmente com Docker Desktop.

Para o ponto extra de producao, basta apresentar a URL publica gerada pelo PythonAnywhere.
