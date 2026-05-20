# Sistema de Agendamento de Caronas

Projeto desenvolvido com Django para a disciplina **GAC116 - Programação Web**.

## Sobre o Projeto

O sistema permite o gerenciamento de caronas entre usuários, possibilitando:

- Cadastro de usuários e perfis
- Cadastro de veículos
- Cadastro de locais de origem e destino
- Oferta de caronas
- Reserva de vagas por passageiros
- Avaliação das viagens realizadas

---

## Checkpoint 1

Esta entrega é focada na modelagem completa do sistema e na configuração do ambiente administrativo do Django.

### Funcionalidades implementadas no Django Admin

- Integração com **Jazzmin** para personalização visual do Django Admin
- Uso de `list_display` para exibição dos principais campos das entidades
- Uso de `list_filter` para filtros rápidos de registros
- Uso de `search_fields` para busca de usuários, rotas, placas e locais
- Uso de `inlines` para facilitar o cadastro relacionado:
  - veículos dentro do perfil do usuário
  - reservas dentro da carona
  - avaliações dentro da reserva
- Validações utilizando `clean()` nos modelos, incluindo:
  - impedimento de cadastro de caronas no passado
  - validação de origem e destino diferentes
  - bloqueio do motorista reservar a própria carona
  - controle de limite máximo de vagas

---

## Modelagem

### Entidades principais

- `PerfilUsuario` → dados complementares do usuário autenticável
- `Veiculo` → veículos vinculados aos motoristas
- `Local` → pontos de origem e destino
- `Carona` → oferta de viagem contendo motorista, veículo, rota, horário, valor e vagas
- `Reserva` → solicitação/confirmação de vaga por passageiros
- `Avaliacao` → nota e comentário associados à reserva

O diagrama entidade-relacionamento está disponível em:

[MODELAGEM_ER.md](MODELAGEM_ER.md).


---

## Tecnologias Utilizadas

- Python
- Django
- SQLite
- Jazzmin

---

## Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/GustavoHMFilho/sistema-agendamento-caronas
```

### 2. Entrar na pasta do projeto

```bash
cd nome-do-projeto
```

### 3. Criar o ambiente virtual

#### Windows

```bash
python -m venv .venv
```

#### Linux/macOS

```bash
python3 -m venv .venv
```

---

### 4. Ativar o ambiente virtual

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux/macOS

```bash
source .venv/bin/activate
```

---

### 5. Instalar as dependências

```bash
pip install -r requirements.txt
```

---

### 6. Executar as migrações

```bash
python manage.py migrate
```

---

### 7. Criar um superusuário

```bash
python manage.py createsuperuser
```

---

### 8. Iniciar o servidor

```bash
python manage.py runserver
```

---

## Acesso ao Sistema

Após iniciar o servidor, acesse:

```text
http://127.0.0.1:8000/admin/
```

---

## Estrutura Geral do Sistema

O sistema foi desenvolvido seguindo a arquitetura padrão do Django, utilizando:

- Models para persistência dos dados
- Django Admin para gerenciamento administrativo
- Relacionamentos entre entidades com `ForeignKey` e `OneToOneField`
- Validações de negócio diretamente nos modelos
