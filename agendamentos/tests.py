from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Carona, Local, PerfilUsuario, Reserva, Veiculo


class AreaUsuarioTests(TestCase):
    def setUp(self):
        self.motorista_user = User.objects.create_user(username='motorista', password='teste123')
        self.passageiro_user = User.objects.create_user(username='passageiro', password='teste123')
        self.motorista = PerfilUsuario.objects.create(
            usuario=self.motorista_user,
            telefone='35999990000',
            tipo=PerfilUsuario.TipoUsuario.MOTORISTA,
        )
        self.passageiro = PerfilUsuario.objects.create(
            usuario=self.passageiro_user,
            telefone='35999991111',
            tipo=PerfilUsuario.TipoUsuario.PASSAGEIRO,
        )
        self.veiculo = Veiculo.objects.create(
            motorista=self.motorista,
            modelo='Fiat Uno',
            placa='ABC1D23',
            cor='Prata',
            capacidade=4,
        )
        self.origem = Local.objects.create(nome='UFLA', endereco='Campus Universitario')
        self.destino = Local.objects.create(nome='Centro', endereco='Praca Central')
        self.carona = Carona.objects.create(
            motorista=self.motorista,
            veiculo=self.veiculo,
            origem=self.origem,
            destino=self.destino,
            data_hora_saida=timezone.now() + timedelta(days=1),
            valor_por_vaga=5,
            vagas_disponiveis=3,
        )

    def test_dashboard_exige_login(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_usuario_logado_visualiza_caronas(self):
        self.client.login(username='passageiro', password='teste123')

        response = self.client.get(reverse('listar_caronas'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'UFLA')
        self.assertContains(response, 'Centro')

    def test_passageiro_reserva_carona(self):
        self.client.login(username='passageiro', password='teste123')

        response = self.client.post(reverse('reservar_carona', args=[self.carona.pk]), {'observacao': 'Saio da biblioteca.'})

        self.assertRedirects(response, reverse('minhas_reservas'))
        self.assertTrue(
            Reserva.objects.filter(
                carona=self.carona,
                passageiro=self.passageiro,
                status=Reserva.Status.CONFIRMADA,
            ).exists()
        )
