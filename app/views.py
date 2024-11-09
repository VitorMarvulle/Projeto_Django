from datetime import timedelta
from django.shortcuts import render,redirect

#importa a funcao get_template() do módulo loader
from app.forms import FormCadastroUser, FormCadastroCurso, FormLogin, FormFoto, FormContato
from django.contrib import messages
from app.models import Usuario, Curso, Foto
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout

def app(request):
    
    email_do_usuario = request.session.get('email')

    context = {
        'email_do_usuario': email_do_usuario,
     }
    return render(request, 'index.html', context)

def cadastrar_user(request):
    novo_user = FormCadastroUser(request.POST or None, request.FILES or None)
    
    # SALVAR USUÁRIO
    if request.method == 'POST':
        if novo_user.is_valid():
            usuario = novo_user.save(commit=False)  # Evita salvar imediatamente no banco
            # Criptografa a senha antes de salvar
            usuario.senha = make_password(novo_user.cleaned_data['senha'])
            usuario.save()  # Agora salva com a senha criptografada
            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect('app')  # Redireciona para a página principal ou de login
    
    context = {
        'form': novo_user
    }

    return render(request, 'cadastro.html', context)

def cadastrar_curso(request):
    novo_curso = FormCadastroCurso(request.POST or None, request.FILES or None)
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
    usuarios = Usuario.objects.all()

    context = {
        'dados' : usuarios
    }

    return render(request, 'usuarios.html', context)

def exibir_curso(request):
    cursos = Curso.objects.all()

    context = {
        'cursos' : cursos
    }

    return render(request, 'cursos.html', context)

def dashboard(request):
    if not request.session.get('email'):
        return redirect('fazerlogin')

    email = request.session['email']
    usuario = Usuario.objects.get(email=email)

    context = {
        'usuario': usuario
    }
    
    return render(request, 'dashboard.html', context)

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
                request.session.set_expiry(30)  # Sessão de 30 segundos
                request.session['email'] = _email
                messages.success(request, 'Login bem-sucedido!')
                return redirect('dashboard')  # Redireciona para o dashboard
            else:
                messages.error(request, 'Credenciais inválidas. Por favor, tente novamente!')
        except Usuario.DoesNotExist:
            messages.error(request, 'Credenciais inválidas. Por favor, tente novamente!')
    
    return render(request, 'login.html', {'formLogin': formL})

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

def excluir_conta(request):
    if not request.session.get('email'):
        return redirect('fazerlogin')
    
    email = request.session['email']
    usuario = Usuario.objects.get(email=email)

    # Exclui o usuário
    usuario.delete()
    
    # Limpa a sessão do usuário
    request.session.flush()  
    
    # Redireciona para a página inicial
    messages.success(request, 'Conta excluída com sucesso.')
    return redirect('app')  # Ou o nome da sua página inicial

def alterar_senha(request):
    if not request.session.get('email'):
        return redirect('fazerlogin')

    if request.method == 'POST':
        email = request.session['email']
        usuario = Usuario.objects.get(email=email)
        
        senha_atual = request.POST.get('senha_atual')
        nova_senha = request.POST.get('nova_senha')
        confirmacao_senha = request.POST.get('confirmacao_senha')

        # Verifica se a senha atual está correta
        if not check_password(senha_atual, usuario.senha):
            messages.error(request, 'A senha atual está incorreta.')
            return render(request, 'alterar_senha.html')

        # Verifica se a nova senha e a confirmação coincidem
        if nova_senha != confirmacao_senha:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'alterar_senha.html')

        # Atualiza a senha
        usuario.senha = make_password(nova_senha)  # Criptografa a nova senha
        usuario.save()
        messages.success(request, 'Senha alterada com sucesso!')
        return redirect('dashboard')

    return render(request, 'alterar_senha.html')

def add_foto(request):
    if request.method == 'POST':
        form = FormFoto(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('galeria')
    else:
        form = FormFoto()
    return render (request, 'add_foto.html', {'form': form})

def galeria(request):
    fotos = Foto.objects.all().values()

    context = {
        'galeria' : fotos
    }
    return render (request, 'galeria.html', context)

def excluir_curso(request, id_curso):
    curso = Curso.objects.get(id=id_curso)
    curso.delete()
    return redirect('exibir_curso')

def contato(request):
    novo_contato = FormContato(request.POST or None)
    
    # SALVAR USUÁRIO
    if request.method == 'POST':
        if novo_contato.is_valid():
            contato = novo_contato.save(commit=True)
            messages.success(request, "Mensagem enviada com sucesso!")
            return redirect('app')  # Redireciona para a página principal ou de login
    
    context = {
        'form': novo_contato
    }

    return render(request, 'contato.html', context)
