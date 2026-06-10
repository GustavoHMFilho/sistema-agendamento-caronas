from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from agendamentos.models import Carona, Local, PerfilUsuario, Veiculo


class Command(BaseCommand):
    help = 'Cria dados de demonstracao para testar o sistema de caronas.'

    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True},
        )
        if created:
            admin.set_password('admin123')
            admin.save()

        motorista_user, created = User.objects.get_or_create(
            username='motorista',
            defaults={'first_name': 'Marina', 'last_name': 'Silva', 'email': 'motorista@example.com'},
        )
        if created:
            motorista_user.set_password('teste123')
            motorista_user.save()

        passageiro_user, created = User.objects.get_or_create(
            username='passageiro',
            defaults={'first_name': 'Pedro', 'last_name': 'Souza', 'email': 'passageiro@example.com'},
        )
        if created:
            passageiro_user.set_password('teste123')
            passageiro_user.save()

        motorista, _ = PerfilUsuario.objects.get_or_create(
            usuario=motorista_user,
            defaults={
                'telefone': '(35) 99999-1000',
                'matricula': '20261001',
                'tipo': PerfilUsuario.TipoUsuario.MOTORISTA,
            },
        )
        passageiro, _ = PerfilUsuario.objects.get_or_create(
            usuario=passageiro_user,
            defaults={
                'telefone': '(35) 99999-2000',
                'matricula': '20261002',
                'tipo': PerfilUsuario.TipoUsuario.PASSAGEIRO,
            },
        )

        origem, _ = Local.objects.get_or_create(
            nome='UFLA',
            cidade='Lavras',
            defaults={'endereco': 'Campus Universitario', 'ponto_referencia': 'Portaria principal'},
        )
        destino, _ = Local.objects.get_or_create(
            nome='Centro',
            cidade='Lavras',
            defaults={'endereco': 'Praca Dr. Augusto Silva', 'ponto_referencia': 'Centro da cidade'},
        )
        Local.objects.get_or_create(
            nome='Rodoviaria',
            cidade='Lavras',
            defaults={'endereco': 'Terminal Rodoviario de Lavras', 'ponto_referencia': 'Embarque principal'},
        )

        veiculo, _ = Veiculo.objects.get_or_create(
            motorista=motorista,
            placa='ABC1D23',
            defaults={'modelo': 'Fiat Uno', 'cor': 'Prata', 'capacidade': 4},
        )

        Carona.objects.get_or_create(
            motorista=motorista,
            veiculo=veiculo,
            origem=origem,
            destino=destino,
            status=Carona.Status.AGENDADA,
            defaults={
                'data_hora_saida': timezone.now() + timedelta(days=1),
                'valor_por_vaga': 5,
                'vagas_disponiveis': 3,
                'observacoes': 'Saida em frente a biblioteca universitaria.',
            },
        )

        self.stdout.write(self.style.SUCCESS('Dados de demonstracao criados com sucesso.'))
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('Motorista: motorista / teste123')
        self.stdout.write('Passageiro: passageiro / teste123')
