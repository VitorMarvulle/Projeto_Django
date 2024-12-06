#importa a função path do modulo django.urls para definir os padrões de URL
from django.urls import path

#importe o módulo views do diretório atual
from . import views

#lista de objetos path, define padrões de URL
urlpatterns = [
    #define a view a ser chamada quando a URL é acessada
    
    path('' , views.app, name="app"),
    path('login/' , views.fazerlogin, name="fazerlogin"),
    path('cadastro/' , views.cadastrar_user, name="cadastrar_user"),
    path('usuarios/' , views.exibir_user, name="exibir_user"),
    path('cursos/' , views.exibir_curso, name="exibir_curso"),
    path('cadastro_curso/' , views.cadastrar_curso, name="cadastrar_curso"),
    
    #editar e excluir
    path('editar_usuario/<int:id_usuario>' , views.editar_usuario, name="editar_usuario"),
    path('excluir_usuario/<int:id_usuario>' , views.excluir_usuario, name="excluir_usuario"),

    #dashboard
    path('dashboard/', views.dashboard, name="dashboard"),
    path('alterar_senha/', views.alterar_senha, name='alterar_senha'),
    path('excluir_conta/', views.excluir_conta, name='excluir_conta'),
    path('logout/', views.userLogout, name='logout'),


    #foto
    path('add-foto/', views.add_foto, name='add_foto'),
    path('galeria/', views.galeria, name='galeria'),

    #projetos
    path('excluir_curso/<int:id_curso>', views.excluir_curso, name='excluir_curso'),
    path('realizar_venda/<int:id_curso>', views.realizar_venda, name='realizar_venda'),

    #contato
    path('contato', views.contato, name='contato'),

    #grafico
    path('grafico_mes/', views.grafico_mes, name='grafico_mes'),  
    path('grafico_diario/', views.grafico_diario, name='grafico_diario'),
]