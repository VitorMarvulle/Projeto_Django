from datetime import timedelta
from django.shortcuts import render,redirect
from django.http import HttpResponse

#importa a funcao get_template() do módulo loader
from django.template import loader
from app.forms import FormCadastroUser, FormCadastroCurso, FormLogin
from django.contrib import messages
from app.models import Usuario, Curso, Login

def app(request):
    
    email_do_usuario = request.session.get('email')

    context = {
        'email_do_usuario': email_do_usuario,
     }
    return render(request, 'index.html', context)

def cadastrar_user(request):
    novo_user = FormCadastroUser(request.POST or None)
    #SALVAR USUÁRIO
    if request.POST:
        if novo_user. is_valid():
            novo_user.save()
            messages.success(request, "Usuário Cadastrado com sucesso!")
            return redirect('app')
    context = {
        'form' : novo_user
    }

    return render(request, 'cadastro.html', context)

def cadastrar_curso(request):
    novo_curso = FormCadastroCurso(request.POST or None)
    #SALVAR USUÁRIO
    if request.POST:
        if novo_curso. is_valid():
            novo_curso.save()
            messages.success(request, "Curso Cadastrado com sucesso!")
            return redirect('app')
    context = {
        'form' : novo_curso
    }

    return render(request, 'cadastro_curso.html', context)

def exibir_user(request):
    usuarios = Usuario.objects.all().values()

    context = {
        'dados' : usuarios
    }

    return render(request, 'usuarios.html', context)

def exibir_curso(request):
    cursos = Curso.objects.all().values()

    context = {
        'cursos' : cursos
    }

    return render(request, 'cursos.html', context)

def fazerlogin(request):
    formL = FormLogin(request.POST or None)
    
    if request.method == 'POST':
        if formL.is_valid():
            _email = formL.cleaned_data.get('email')
            _senha = formL.cleaned_data.get('senha')
            try:
                usuarioL = Login.objects.get(email=_email, senha=_senha)
                if usuarioL:
                    # Define a duração da sessão como 30 segundos
                    request.session.set_expiry(timedelta(seconds=30))
                    # Cria uma sessão com o email do usuário
                    request.session['email'] = _email
                    return redirect('app')  # Altere 'app' para a URL que você deseja redirecionar
            except Login.DoesNotExist:
                messages.error(request, 'Credenciais inválidas. Por favor, tente novamente!')
    
    context = {
        'formLogin': formL
    }
    return render(request, 'login.html', context)