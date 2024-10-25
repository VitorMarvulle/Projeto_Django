from datetime import timedelta
from django.shortcuts import render,redirect

#importa a funcao get_template() do módulo loader
from app.forms import FormCadastroUser, FormCadastroCurso, FormLogin
from django.contrib import messages
from app.models import Usuario, Curso
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout

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
        _email = request.POST.get('email')
        _senha = request.POST.get('senha')

        if not _email or not _senha:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return render(request, 'login.html', {'formLogin': formL})

        try:
            usuarioL = Usuario.objects.get(email=_email)
            if check_password(_senha, usuarioL.senha):  
                request.session.set_expiry(timedelta(seconds=30))
                request.session['email'] = _email
                return redirect('app') 
            else:
                messages.error(request, 'Credenciais inválidas. Por favor, tente novamente!')
        except Usuario.DoesNotExist:
            messages.error(request, 'Credenciais inválidas. Por favor, tente novamente!')

    context = {
        'formLogin': formL
    }
    return render(request, 'login.html', context)

def editar_usuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    form = FormCadastroUser(request.POST or None, instance=usuario)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('exibir_user')
    context = {
            'form' : form
        }
    return render(request, 'editar_usuario.html', context)

def excluir_usuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    usuario.delete()
    return redirect('exibir_user')