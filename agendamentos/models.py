from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class PerfilUsuario(models.Model):
    class TipoUsuario(models.TextChoices):
        PASSAGEIRO = 'PASSAGEIRO', 'Passageiro'
        MOTORISTA = 'MOTORISTA', 'Motorista'
        AMBOS = 'AMBOS', 'Passageiro e motorista'

    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20)
    tipo = models.CharField(max_length=20, choices=TipoUsuario.choices, default=TipoUsuario.PASSAGEIRO)
    matricula = models.CharField(max_length=20, blank=True, verbose_name='matricula')
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'perfil de usuario'
        verbose_name_plural = 'perfis de usuarios'
        ordering = ['usuario__first_name', 'usuario__username']

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username


class Veiculo(models.Model):
    motorista = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name='veiculos')
    modelo = models.CharField(max_length=80)
    placa = models.CharField(max_length=8, unique=True)
    cor = models.CharField(max_length=30)
    capacidade = models.PositiveSmallIntegerField(default=4)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'veiculo'
        verbose_name_plural = 'veiculos'
        ordering = ['modelo', 'placa']

    def clean(self):
        if self.motorista_id and self.motorista.tipo == PerfilUsuario.TipoUsuario.PASSAGEIRO:
            raise ValidationError({'motorista': 'O proprietario do veiculo deve estar habilitado como motorista.'})
        if self.capacidade < 1:
            raise ValidationError({'capacidade': 'A capacidade deve ser maior que zero.'})

    def __str__(self):
        return f'{self.modelo} - {self.placa}'


class Local(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=180)
    cidade = models.CharField(max_length=80, default='Lavras')
    ponto_referencia = models.CharField(max_length=120, blank=True)

    class Meta:
        verbose_name = 'local'
        verbose_name_plural = 'locais'
        ordering = ['cidade', 'nome']
        unique_together = ('nome', 'cidade')

    def __str__(self):
        return f'{self.nome} ({self.cidade})'


class Carona(models.Model):
    class Status(models.TextChoices):
        AGENDADA = 'AGENDADA', 'Agendada'
        EM_ANDAMENTO = 'EM_ANDAMENTO', 'Em andamento'
        FINALIZADA = 'FINALIZADA', 'Finalizada'
        CANCELADA = 'CANCELADA', 'Cancelada'

    motorista = models.ForeignKey(PerfilUsuario, on_delete=models.PROTECT, related_name='caronas_oferecidas')
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, related_name='caronas')
    origem = models.ForeignKey(Local, on_delete=models.PROTECT, related_name='caronas_origem')
    destino = models.ForeignKey(Local, on_delete=models.PROTECT, related_name='caronas_destino')
    data_hora_saida = models.DateTimeField()
    valor_por_vaga = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    vagas_disponiveis = models.PositiveSmallIntegerField()
    observacoes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AGENDADA)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'carona'
        verbose_name_plural = 'caronas'
        ordering = ['-data_hora_saida']

    def clean(self):
        errors = {}

        if self.origem_id and self.destino_id and self.origem_id == self.destino_id:
            errors['destino'] = 'Origem e destino devem ser locais diferentes.'

        if self.veiculo_id and self.motorista_id and self.veiculo.motorista_id != self.motorista_id:
            errors['veiculo'] = 'O veiculo selecionado precisa pertencer ao motorista da carona.'

        if self.motorista_id and self.motorista.tipo == PerfilUsuario.TipoUsuario.PASSAGEIRO:
            errors['motorista'] = 'O motorista deve ter perfil de motorista ou passageiro e motorista.'

        if self.data_hora_saida and self.data_hora_saida < timezone.now() and self.status == self.Status.AGENDADA:
            errors['data_hora_saida'] = 'Nao e permitido agendar uma carona no passado.'

        if self.veiculo_id and self.vagas_disponiveis > self.veiculo.capacidade:
            errors['vagas_disponiveis'] = 'As vagas nao podem ultrapassar a capacidade do veiculo.'

        if errors:
            raise ValidationError(errors)

    @property
    def vagas_reservadas(self):
        return self.reservas.filter(status=Reserva.Status.CONFIRMADA).count()

    @property
    def vagas_restantes(self):
        return max(self.vagas_disponiveis - self.vagas_reservadas, 0)

    def __str__(self):
        return f'{self.origem} -> {self.destino} em {self.data_hora_saida:%d/%m/%Y %H:%M}'


class Reserva(models.Model):
    class Status(models.TextChoices):
        SOLICITADA = 'SOLICITADA', 'Solicitada'
        CONFIRMADA = 'CONFIRMADA', 'Confirmada'
        CANCELADA = 'CANCELADA', 'Cancelada'

    carona = models.ForeignKey(Carona, on_delete=models.CASCADE, related_name='reservas')
    passageiro = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name='reservas')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SOLICITADA)
    criado_em = models.DateTimeField(auto_now_add=True)
    observacao = models.CharField(max_length=160, blank=True)

    class Meta:
        verbose_name = 'reserva'
        verbose_name_plural = 'reservas'
        ordering = ['-criado_em']
        unique_together = ('carona', 'passageiro')

    def clean(self):
        errors = {}

        if self.carona_id and self.passageiro_id and self.carona.motorista_id == self.passageiro_id:
            errors['passageiro'] = 'O motorista nao pode reservar vaga na propria carona.'

        if self.carona_id and self.carona.status == Carona.Status.CANCELADA:
            errors['carona'] = 'Nao e possivel reservar uma carona cancelada.'

        if self.status == self.Status.CONFIRMADA and self.carona_id:
            reservas_confirmadas = self.carona.reservas.filter(status=self.Status.CONFIRMADA)
            if self.pk:
                reservas_confirmadas = reservas_confirmadas.exclude(pk=self.pk)
            if reservas_confirmadas.count() >= self.carona.vagas_disponiveis:
                errors['status'] = 'Nao ha vagas disponiveis para confirmar esta reserva.'

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f'{self.passageiro} - {self.carona}'


class Avaliacao(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, related_name='avaliacao')
    nota = models.PositiveSmallIntegerField()
    comentario = models.TextField(blank=True)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'avaliacao'
        verbose_name_plural = 'avaliacoes'
        ordering = ['-criada_em']

    def clean(self):
        if self.nota < 1 or self.nota > 5:
            raise ValidationError({'nota': 'A nota deve estar entre 1 e 5.'})

    def __str__(self):
        return f'Nota {self.nota} para {self.reserva.carona}'
