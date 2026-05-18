# Modelagem Entidade-Relacionamento

Sistema de agendamento de caronas.

```mermaid
erDiagram
    USER ||--|| PERFIL_USUARIO : possui
    PERFIL_USUARIO ||--o{ VEICULO : possui
    PERFIL_USUARIO ||--o{ CARONA : oferece
    VEICULO ||--o{ CARONA : utilizado_em
    LOCAL ||--o{ CARONA : origem
    LOCAL ||--o{ CARONA : destino
    CARONA ||--o{ RESERVA : recebe
    PERFIL_USUARIO ||--o{ RESERVA : realiza
    RESERVA ||--o| AVALIACAO : gera

    USER {
        bigint id PK
        string username
        string first_name
        string last_name
        string email
        string password
        boolean is_staff
        boolean is_active
    }

    PERFIL_USUARIO {
        bigint id PK
        bigint usuario_id FK
        string telefone
        string tipo
        string matricula
        boolean ativo
    }

    VEICULO {
        bigint id PK
        bigint motorista_id FK
        string modelo
        string placa UK
        string cor
        int capacidade
        boolean ativo
    }

    LOCAL {
        bigint id PK
        string nome
        string endereco
        string cidade
        string ponto_referencia
    }

    CARONA {
        bigint id PK
        bigint motorista_id FK
        bigint veiculo_id FK
        bigint origem_id FK
        bigint destino_id FK
        datetime data_hora_saida
        decimal valor_por_vaga
        int vagas_disponiveis
        text observacoes
        string status
        datetime criado_em
    }

    RESERVA {
        bigint id PK
        bigint carona_id FK
        bigint passageiro_id FK
        string status
        datetime criado_em
        string observacao
    }

    AVALIACAO {
        bigint id PK
        bigint reserva_id FK
        int nota
        text comentario
        datetime criada_em
    }
```

## Entidades

| Entidade | Descricao |
| --- | --- |
| `User` | Usuario autenticavel do Django, usado para login e permissao de acesso. |
| `PerfilUsuario` | Complementa o usuario com telefone, tipo de uso e matricula. |
| `Veiculo` | Veiculo cadastrado por um motorista para oferecer caronas. |
| `Local` | Ponto de origem ou destino das caronas. |
| `Carona` | Oferta de viagem cadastrada por um motorista, com rota, horario, valor e vagas. |
| `Reserva` | Solicitacao ou confirmacao de vaga feita por um passageiro. |
| `Avaliacao` | Nota e comentario associados a uma reserva realizada. |

## Regras e Cardinalidades

| Relacionamento | Cardinalidade | Regra |
| --- | --- | --- |
| `User` - `PerfilUsuario` | 1:1 | Cada usuario possui um unico perfil complementar. |
| `PerfilUsuario` - `Veiculo` | 1:N | Um motorista pode cadastrar varios veiculos. |
| `PerfilUsuario` - `Carona` | 1:N | Um motorista pode oferecer varias caronas. |
| `Veiculo` - `Carona` | 1:N | Um veiculo pode ser usado em varias caronas. |
| `Local` - `Carona` | 1:N | Um local pode aparecer como origem ou destino em varias caronas. |
| `Carona` - `Reserva` | 1:N | Uma carona pode receber varias reservas. |
| `PerfilUsuario` - `Reserva` | 1:N | Um passageiro pode realizar varias reservas. |
| `Reserva` - `Avaliacao` | 1:0..1 | Uma reserva pode ter no maximo uma avaliacao. |

## Principais Restricoes

- A placa do veiculo deve ser unica.
- Um usuario so pode ter um perfil.
- A mesma pessoa nao pode reservar a mesma carona mais de uma vez.
- Origem e destino da carona devem ser diferentes.
- O motorista nao pode reservar vaga na propria carona.
- Nao e permitido confirmar reservas acima do numero de vagas disponiveis.
- A nota da avaliacao deve estar entre 1 e 5.
