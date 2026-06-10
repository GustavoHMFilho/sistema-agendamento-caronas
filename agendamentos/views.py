from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    AvaliacaoForm,
    CadastroUsuarioForm,
    CaronaForm,
    LocalForm,
    PerfilUsuarioForm,
    ReservaForm,
    VeiculoForm,
)
from .models import Avaliacao, Carona, PerfilUsuario, Reserva, Veiculo


def obter_perfil(user):
    perfil, _ = PerfilUsuario.objects.get_or_create(
        usuario=user,
        defaults={'telefone': '', 'tipo': PerfilUsuario.TipoUsuario.PASSAGEIRO},
    )
    return perfil


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso.')
            return redirect('dashboard')
    else:
        form = CadastroUsuarioForm()

    return render(request, 'registration/cadastro.html', {'form': form})


@login_required
def dashboard(request):
    perfil = obter_perfil(request.user)
    proximas_caronas = Carona.objects.filter(
        status=Carona.Status.AGENDADA,
        data_hora_saida__gte=timezone.now(),
    ).select_related('motorista', 'origem', 'destino', 'veiculo')[:5]
    minhas_reservas = Reserva.objects.filter(passageiro=perfil).select_related(
        'carona',
        'carona__origem',
        'carona__destino',
    )[:5]
    minhas_caronas = Carona.objects.filter(motorista=perfil).select_related('origem', 'destino')[:5]

    contexto = {
        'perfil': perfil,
        'proximas_caronas': proximas_caronas,
        'minhas_reservas': minhas_reservas,
        'minhas_caronas': minhas_caronas,
    }
    return render(request, 'agendamentos/dashboard.html', contexto)


@login_required
def editar_perfil(request):
    perfil = obter_perfil(request.user)

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado.')
            return redirect('dashboard')
    else:
        form = PerfilUsuarioForm(instance=perfil)

    return render(request, 'agendamentos/form.html', {'form': form, 'titulo': 'Editar perfil'})


@login_required
def listar_caronas(request):
    termo = request.GET.get('q', '').strip()
    caronas = Carona.objects.filter(
        status=Carona.Status.AGENDADA,
        data_hora_saida__gte=timezone.now(),
    ).select_related('motorista', 'motorista__usuario', 'veiculo', 'origem', 'destino')

    if termo:
        caronas = caronas.filter(
            Q(origem__nome__icontains=termo)
            | Q(destino__nome__icontains=termo)
            | Q(origem__cidade__icontains=termo)
            | Q(destino__cidade__icontains=termo)
            | Q(motorista__usuario__first_name__icontains=termo)
            | Q(motorista__usuario__username__icontains=termo)
        )

    return render(request, 'agendamentos/carona_lista.html', {'caronas': caronas, 'termo': termo})


@login_required
def detalhe_carona(request, pk):
    perfil = obter_perfil(request.user)
    carona = get_object_or_404(
        Carona.objects.select_related('motorista', 'motorista__usuario', 'veiculo', 'origem', 'destino'),
        pk=pk,
    )
    reserva = Reserva.objects.filter(carona=carona, passageiro=perfil).first()

    return render(
        request,
        'agendamentos/carona_detalhe.html',
        {'carona': carona, 'reserva': reserva, 'perfil': perfil},
    )


@login_required
def criar_carona(request):
    perfil = obter_perfil(request.user)
    if perfil.tipo == PerfilUsuario.TipoUsuario.PASSAGEIRO:
        messages.warning(request, 'Atualize seu perfil para motorista antes de oferecer uma carona.')
        return redirect('editar_perfil')

    if not perfil.veiculos.filter(ativo=True).exists():
        messages.warning(request, 'Cadastre um veiculo ativo antes de oferecer uma carona.')
        return redirect('criar_veiculo')

    if request.method == 'POST':
        form = CaronaForm(request.POST, motorista=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Carona cadastrada com sucesso.')
            return redirect('minhas_caronas')
    else:
        form = CaronaForm(motorista=perfil)

    return render(request, 'agendamentos/form.html', {'form': form, 'titulo': 'Oferecer carona'})


@login_required
def minhas_caronas(request):
    perfil = obter_perfil(request.user)
    reservas = Reserva.objects.select_related('passageiro', 'passageiro__usuario').order_by('-criado_em')
    caronas = (
        Carona.objects.filter(motorista=perfil)
        .select_related('origem', 'destino', 'veiculo')
        .prefetch_related(Prefetch('reservas', queryset=reservas))
    )
    return render(request, 'agendamentos/minhas_caronas.html', {'caronas': caronas})


@login_required
def cancelar_carona(request, pk):
    perfil = obter_perfil(request.user)
    carona = get_object_or_404(Carona, pk=pk, motorista=perfil)

    if request.method == 'POST':
        carona.status = Carona.Status.CANCELADA
        carona.save(update_fields=['status'])
        messages.success(request, 'Carona cancelada.')
        return redirect('minhas_caronas')

    return render(request, 'agendamentos/confirmar.html', {'objeto': carona, 'acao': 'cancelar esta carona'})


@login_required
def reservar_carona(request, pk):
    perfil = obter_perfil(request.user)
    carona = get_object_or_404(Carona, pk=pk, status=Carona.Status.AGENDADA)

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.carona = carona
            reserva.passageiro = perfil
            reserva.status = Reserva.Status.SOLICITADA
            try:
                reserva.full_clean()
            except ValidationError as exc:
                form.add_error(None, ' '.join(exc.messages))
            else:
                reserva.save()
                messages.success(request, 'Solicitacao enviada ao motorista.')
                return redirect('minhas_reservas')
    else:
        form = ReservaForm()

    return render(
        request,
        'agendamentos/form.html',
        {'form': form, 'titulo': f'Reservar carona: {carona.origem} para {carona.destino}'},
    )


@login_required
def minhas_reservas(request):
    perfil = obter_perfil(request.user)
    reservas = Reserva.objects.filter(passageiro=perfil).select_related(
        'carona',
        'carona__origem',
        'carona__destino',
        'carona__motorista',
        'carona__motorista__usuario',
    )
    return render(request, 'agendamentos/minhas_reservas.html', {'reservas': reservas})


@login_required
def cancelar_reserva(request, pk):
    perfil = obter_perfil(request.user)
    reserva = get_object_or_404(Reserva, pk=pk, passageiro=perfil)

    if request.method == 'POST':
        reserva.status = Reserva.Status.CANCELADA
        reserva.save(update_fields=['status'])
        messages.success(request, 'Reserva cancelada.')
        return redirect('minhas_reservas')

    return render(request, 'agendamentos/confirmar.html', {'objeto': reserva, 'acao': 'cancelar esta reserva'})


@login_required
def confirmar_reserva_motorista(request, pk):
    perfil = obter_perfil(request.user)
    reserva = get_object_or_404(Reserva, pk=pk, carona__motorista=perfil)

    if request.method != 'POST':
        return redirect('minhas_caronas')

    if reserva.status != Reserva.Status.SOLICITADA:
        messages.info(request, 'Esta reserva nao esta pendente de confirmacao.')
        return redirect('minhas_caronas')

    reserva.status = Reserva.Status.CONFIRMADA
    try:
        reserva.full_clean()
    except ValidationError as exc:
        messages.error(request, ' '.join(exc.messages))
    else:
        reserva.save(update_fields=['status'])
        messages.success(request, f'Reserva de {reserva.passageiro} confirmada.')

    return redirect('minhas_caronas')


@login_required
def recusar_reserva_motorista(request, pk):
    perfil = obter_perfil(request.user)
    reserva = get_object_or_404(Reserva, pk=pk, carona__motorista=perfil)

    if request.method != 'POST':
        return redirect('minhas_caronas')

    if reserva.status == Reserva.Status.CANCELADA:
        messages.info(request, 'Esta reserva ja esta cancelada.')
        return redirect('minhas_caronas')

    reserva.status = Reserva.Status.CANCELADA
    reserva.save(update_fields=['status'])
    messages.success(request, f'Reserva de {reserva.passageiro} recusada/cancelada.')

    return redirect('minhas_caronas')


@login_required
def criar_veiculo(request):
    perfil = obter_perfil(request.user)

    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            veiculo = form.save(commit=False)
            veiculo.motorista = perfil
            try:
                veiculo.full_clean()
            except ValidationError as exc:
                form.add_error(None, ' '.join(exc.messages))
                return render(request, 'agendamentos/form.html', {'form': form, 'titulo': 'Cadastrar veiculo'})

            veiculo.save()
            if perfil.tipo == PerfilUsuario.TipoUsuario.PASSAGEIRO:
                perfil.tipo = PerfilUsuario.TipoUsuario.AMBOS
                perfil.save(update_fields=['tipo'])
            messages.success(request, 'Veiculo cadastrado.')
            return redirect('meus_veiculos')
    else:
        form = VeiculoForm()

    return render(request, 'agendamentos/form.html', {'form': form, 'titulo': 'Cadastrar veiculo'})


@login_required
def meus_veiculos(request):
    perfil = obter_perfil(request.user)
    veiculos = Veiculo.objects.filter(motorista=perfil)
    return render(request, 'agendamentos/meus_veiculos.html', {'veiculos': veiculos})


@login_required
def criar_local(request):
    if request.method == 'POST':
        form = LocalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Local cadastrado.')
            return redirect('criar_carona')
    else:
        form = LocalForm()

    return render(request, 'agendamentos/form.html', {'form': form, 'titulo': 'Cadastrar local'})


@login_required
def avaliar_reserva(request, pk):
    perfil = obter_perfil(request.user)
    reserva = get_object_or_404(Reserva, pk=pk, passageiro=perfil, status=Reserva.Status.CONFIRMADA)

    if hasattr(reserva, 'avaliacao'):
        messages.info(request, 'Esta reserva ja foi avaliada.')
        return redirect('minhas_reservas')

    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.reserva = reserva
            avaliacao.full_clean()
            avaliacao.save()
            messages.success(request, 'Avaliacao registrada.')
            return redirect('minhas_reservas')
    else:
        form = AvaliacaoForm()

    return render(request, 'agendamentos/form.html', {'form': form, 'titulo': 'Avaliar carona'})
