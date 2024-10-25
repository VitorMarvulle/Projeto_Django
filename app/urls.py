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
]