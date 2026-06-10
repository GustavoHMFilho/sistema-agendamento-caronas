# Sistema de Agendamento de Caronas

Projeto Django para a disciplina GAC116 - Programacao Web.

## Tema

O sistema permite cadastrar usuarios, veiculos, locais, caronas ofertadas, reservas de passageiros e avaliacoes das viagens.

## Funcionalidades

- Ambiente administrativo protegido por login e senha.
- Admin personalizado com Jazzmin.
- Ambiente do usuario protegido por login e senha.
- Cadastro de usuarios, perfil, veiculos e locais.
- Oferta de caronas por motoristas.
- Busca e listagem de caronas disponiveis.
- Reserva e cancelamento de vagas.
- Avaliacao de caronas reservadas.
- Interface responsiva com Bootstrap.

## Checkpoint 1

Entrega focada em modelagem completa e ambiente administrativo.

Recursos configurados no admin:

- Jazzmin para substituir o template padrao do Django Admin.
- `list_display` para exibir os principais campos das entidades.
- `list_filter` para filtrar caronas, reservas, usuarios, locais e avaliacoes.
- `search_fields` para localizar registros por usuario, rota, placa e local.
- `inlines` para cadastrar veiculos dentro do perfil, reservas dentro da carona e avaliacao dentro da reserva.
- Validacoes com `clean` nos modelos, como impedimento de carona no passado, origem igual ao destino, motorista reservando a propria carona e reserva acima do limite de vagas.

## Modelagem

Entidades principais:

- `PerfilUsuario`: dados complementares do usuario autenticavel.
- `Veiculo`: veiculos vinculados a motoristas.
- `Local`: pontos de origem e destino.
- `Carona`: oferta de viagem com motorista, veiculo, rota, horario, valor e vagas.
- `Reserva`: solicitacao ou confirmacao de vaga por passageiro.
- `Avaliacao`: nota e comentario vinculados a uma reserva.

O diagrama entidade-relacionamento esta em [MODELAGEM_ER.md](MODELAGEM_ER.md).

## Checkpoint 2

A entrega completa inclui a area do usuario com login, telas responsivas com Bootstrap e fluxo funcional para oferecer caronas, reservar vagas, consultar reservas, cadastrar veiculos e avaliar viagens.

## Como executar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py criar_dados_demo
python manage.py runserver
```

Depois acesse:

- Area do usuario: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

Usuarios de demonstracao criados pelo comando `criar_dados_demo`:

| Perfil | Usuario | Senha |
| --- | --- | --- |
| Administrador | `admin` | `admin123` |
| Motorista | `motorista` | `teste123` |
| Passageiro | `passageiro` | `teste123` |

## Como testar

1. Entre como `passageiro`.
2. Acesse a pagina de caronas disponiveis.
3. Abra os detalhes de uma carona e reserve uma vaga.
4. Confira a reserva em "Minhas reservas".
5. Entre como `motorista`.
6. Cadastre um veiculo, um local ou ofereca uma nova carona.
7. Entre no `/admin/` como `admin` para visualizar a modelagem, filtros, buscas, listas e inlines.
