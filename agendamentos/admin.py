from django.contrib import admin

from .models import Avaliacao, Carona, Local, PerfilUsuario, Reserva, Veiculo


class VeiculoInline(admin.TabularInline):
    model = Veiculo
    extra = 0
    fields = ('modelo', 'placa', 'cor', 'capacidade', 'ativo')


class ReservaInline(admin.TabularInline):
    model = Reserva
    extra = 0
    fields = ('passageiro', 'status', 'criado_em', 'observacao')
    readonly_fields = ('criado_em',)
    autocomplete_fields = ('passageiro',)


class AvaliacaoInline(admin.StackedInline):
    model = Avaliacao
    extra = 0
    fields = ('nota', 'comentario', 'criada_em')
    readonly_fields = ('criada_em',)


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefone', 'tipo', 'matricula', 'ativo')
    list_filter = ('tipo', 'ativo')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'telefone', 'matricula')
    list_editable = ('ativo',)
    inlines = (VeiculoInline,)


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'placa', 'cor', 'capacidade', 'motorista', 'ativo')
    list_filter = ('ativo', 'cor')
    search_fields = ('modelo', 'placa', 'motorista__usuario__username', 'motorista__usuario__first_name')
    autocomplete_fields = ('motorista',)
    list_editable = ('ativo',)


@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'endereco', 'ponto_referencia')
    list_filter = ('cidade',)
    search_fields = ('nome', 'cidade', 'endereco', 'ponto_referencia')


@admin.register(Carona)
class CaronaAdmin(admin.ModelAdmin):
    list_display = (
        'data_hora_saida',
        'origem',
        'destino',
        'motorista',
        'veiculo',
        'status',
        'vagas_disponiveis',
        'vagas_restantes',
        'valor_por_vaga',
    )
    list_filter = ('status', 'origem__cidade', 'destino__cidade', 'data_hora_saida')
    search_fields = (
        'motorista__usuario__username',
        'motorista__usuario__first_name',
        'motorista__usuario__last_name',
        'origem__nome',
        'destino__nome',
        'veiculo__placa',
    )
    autocomplete_fields = ('motorista', 'veiculo', 'origem', 'destino')
    date_hierarchy = 'data_hora_saida'
    inlines = (ReservaInline,)


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('carona', 'passageiro', 'status', 'criado_em')
    list_filter = ('status', 'criado_em', 'carona__status')
    search_fields = (
        'passageiro__usuario__username',
        'passageiro__usuario__first_name',
        'passageiro__usuario__last_name',
        'carona__origem__nome',
        'carona__destino__nome',
    )
    autocomplete_fields = ('carona', 'passageiro')
    inlines = (AvaliacaoInline,)


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('reserva', 'nota', 'criada_em')
    list_filter = ('nota', 'criada_em')
    search_fields = ('reserva__passageiro__usuario__username', 'reserva__carona__origem__nome', 'comentario')
    autocomplete_fields = ('reserva',)
