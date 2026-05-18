# Sistema de Agendamento de Caronas

Projeto Django para a disciplina GAC116 - Programacao Web.

## Tema

O sistema permite cadastrar usuarios, veiculos, locais, caronas ofertadas, reservas de passageiros e avaliacoes das viagens.

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

## Como executar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Depois acesse `http://127.0.0.1:8000/admin/`.
