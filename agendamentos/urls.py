from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('perfil/', views.editar_perfil, name='editar_perfil'),
    path('caronas/', views.listar_caronas, name='listar_caronas'),
    path('caronas/nova/', views.criar_carona, name='criar_carona'),
    path('caronas/<int:pk>/', views.detalhe_carona, name='detalhe_carona'),
    path('caronas/<int:pk>/reservar/', views.reservar_carona, name='reservar_carona'),
    path('minhas-caronas/', views.minhas_caronas, name='minhas_caronas'),
    path('minhas-caronas/<int:pk>/cancelar/', views.cancelar_carona, name='cancelar_carona'),
    path('reservas/<int:pk>/confirmar/', views.confirmar_reserva_motorista, name='confirmar_reserva_motorista'),
    path('reservas/<int:pk>/recusar/', views.recusar_reserva_motorista, name='recusar_reserva_motorista'),
    path('minhas-reservas/', views.minhas_reservas, name='minhas_reservas'),
    path('minhas-reservas/<int:pk>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),
    path('minhas-reservas/<int:pk>/avaliar/', views.avaliar_reserva, name='avaliar_reserva'),
    path('veiculos/', views.meus_veiculos, name='meus_veiculos'),
    path('veiculos/novo/', views.criar_veiculo, name='criar_veiculo'),
    path('locais/novo/', views.criar_local, name='criar_local'),
]
