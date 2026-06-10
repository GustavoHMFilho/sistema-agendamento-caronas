from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Avaliacao, Carona, Local, PerfilUsuario, Reserva, Veiculo


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault('class', 'form-check-input')
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault('class', 'form-select')
            else:
                field.widget.attrs.setdefault('class', 'form-control')


class CadastroUsuarioForm(BootstrapFormMixin, UserCreationForm):
    first_name = forms.CharField(label='Nome')
    last_name = forms.CharField(label='Sobrenome', required=False)
    email = forms.EmailField(label='E-mail')
    telefone = forms.CharField(label='Telefone', max_length=20)
    matricula = forms.CharField(label='Matricula', max_length=20, required=False)
    tipo = forms.ChoiceField(label='Tipo de usuario', choices=PerfilUsuario.TipoUsuario.choices)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'telefone', 'matricula', 'tipo')
        labels = {'username': 'Usuario'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            PerfilUsuario.objects.create(
                usuario=user,
                telefone=self.cleaned_data['telefone'],
                matricula=self.cleaned_data['matricula'],
                tipo=self.cleaned_data['tipo'],
            )

        return user


class PerfilUsuarioForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ('telefone', 'tipo', 'matricula', 'ativo')
        labels = {
            'telefone': 'Telefone',
            'tipo': 'Tipo de usuario',
            'matricula': 'Matricula',
            'ativo': 'Perfil ativo',
        }


class VeiculoForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ('modelo', 'placa', 'cor', 'capacidade', 'ativo')
        labels = {
            'modelo': 'Modelo',
            'placa': 'Placa',
            'cor': 'Cor',
            'capacidade': 'Capacidade',
            'ativo': 'Ativo',
        }

    def clean_placa(self):
        return self.cleaned_data['placa'].upper().strip()


class LocalForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Local
        fields = ('nome', 'endereco', 'cidade', 'ponto_referencia')
        labels = {
            'nome': 'Nome',
            'endereco': 'Endereco',
            'cidade': 'Cidade',
            'ponto_referencia': 'Ponto de referencia',
        }


class CaronaForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Carona
        fields = (
            'veiculo',
            'origem',
            'destino',
            'data_hora_saida',
            'valor_por_vaga',
            'vagas_disponiveis',
            'observacoes',
        )
        labels = {
            'veiculo': 'Veiculo',
            'origem': 'Origem',
            'destino': 'Destino',
            'data_hora_saida': 'Data e hora de saida',
            'valor_por_vaga': 'Valor por vaga',
            'vagas_disponiveis': 'Vagas disponiveis',
            'observacoes': 'Observacoes',
        }
        widgets = {
            'data_hora_saida': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, motorista=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.motorista = motorista
        if motorista:
            self.fields['veiculo'].queryset = motorista.veiculos.filter(ativo=True)
        self.fields['origem'].queryset = Local.objects.all()
        self.fields['destino'].queryset = Local.objects.all()

    def clean_data_hora_saida(self):
        data_hora_saida = self.cleaned_data['data_hora_saida']
        if data_hora_saida < timezone.now():
            raise ValidationError('Informe uma data futura para a carona.')
        return data_hora_saida

    def save(self, commit=True):
        carona = super().save(commit=False)
        if self.motorista:
            carona.motorista = self.motorista
        carona.status = Carona.Status.AGENDADA

        if commit:
            carona.full_clean()
            carona.save()

        return carona


class ReservaForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ('observacao',)
        labels = {'observacao': 'Observacao para o motorista'}


class AvaliacaoForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ('nota', 'comentario')
        labels = {'nota': 'Nota', 'comentario': 'Comentario'}
        widgets = {'comentario': forms.Textarea(attrs={'rows': 4})}

    def clean_nota(self):
        nota = self.cleaned_data['nota']
        if nota < 1 or nota > 5:
            raise ValidationError('A nota deve estar entre 1 e 5.')
        return nota
