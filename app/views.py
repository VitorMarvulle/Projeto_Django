from datetime import timezone
from django.shortcuts import get_object_or_404, render,redirect

#importa a funcao get_template() do módulo loader
from app.forms import FormCadastroUser, FormCadastroCurso, FormLogin, FormFoto, FormContato
from django.contrib import messages
from app.models import Usuario, Curso, Foto, Venda
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout

##Grafico
from django.shortcuts import render
import io
import urllib, base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay
from datetime import datetime
from django.utils import timezone  




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
    if not request.session.get('email'):
        messages.error(request, "Faça seu login para cadastrar seu portfólio!")
        return redirect('fazerlogin')
    
    novo_curso = FormCadastroCurso(request.POST or None, request.FILES or None)
    #SALVAR USUÁRIO
    if request.POST:
        if novo_curso. is_valid():
            novo_curso.save()
            messages.success(request, "Curso Cadastrado com sucesso!")
            return redirect('exibir_curso')
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
                request.session.set_expiry(3000)  # Sessão de 30 segundos
                request.session['email'] = _email
                request.session['nome'] = usuarioL.nome
                messages.success(request, 'Login bem-sucedido!')
                return redirect('dashboard')  # Redireciona para o dashboard
            else:
                messages.error(request, 'Credenciais inválidas. Por favor, tente novamente!')
        except Usuario.DoesNotExist:
            messages.error(request, 'Credenciais inválidas. Por favor, tente novamente!')
    
    return render(request, 'login.html', {'formLogin': formL})

def editar_usuario(request, id_usuario):
    if not request.session.get('email'):
        messages.error(request, "Faça seu login para Editar ou Excluir contas!")
        return redirect('fazerlogin')

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
    if not request.session.get('email'):
        messages.error(request, "Faça seu login para Editar ou Excluir contas!")
        return redirect('fazerlogin')

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
    # Buscando as fotos de cada modelo
    usuarios_fotos = Usuario.objects.all()
    cursos_fotos = Curso.objects.all()
    fotos_fotos = Foto.objects.all()

    # Passando as fotos para o contexto
    context = {
        'usuarios_fotos': usuarios_fotos,
        'cursos_fotos': cursos_fotos,
        'fotos_fotos': fotos_fotos,
    }
    
    return render(request, 'galeria.html', context)

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

def userLogout (request):

    logout(request)
    messages.success(request, 'A sessao foi encerrada!')
    return redirect('app')

def realizar_venda(request, id_curso):
    # Recupera o curso com base no ID
    curso = get_object_or_404(Curso, id=id_curso)
    
    try:
        # Reduz o estoque do curso
        curso.reduzir_estoque()

        # Cria o registro da venda
        Venda.objects.create(
            id_curso=curso.id, 
            nome_curso=curso.nome_curso, 
            valor_total=curso.preco * 1  
        )

        messages.success(request, "Compra realizada com sucesso!")
        return redirect('exibir_curso')  
    except ValueError as e:
        # Lida com erros, como estoque insuficiente
        messages.error(request, str(e))
        return redirect('exibir_curso')

##Graficos

def grafico_mes(request):
    # Criar intervalos para cada mês do ano, com suporte a fuso horário
    intervalo_meses = {
        'Jan': (timezone.make_aware(datetime(datetime.now().year, 1, 1)), timezone.make_aware(datetime(datetime.now().year, 1, 31))),
        'Fev': (timezone.make_aware(datetime(datetime.now().year, 2, 1)), timezone.make_aware(datetime(datetime.now().year, 2, 28))),
        'Mar': (timezone.make_aware(datetime(datetime.now().year, 3, 1)), timezone.make_aware(datetime(datetime.now().year, 3, 31))),
        'Abr': (timezone.make_aware(datetime(datetime.now().year, 4, 1)), timezone.make_aware(datetime(datetime.now().year, 4, 30))),
        'Mai': (timezone.make_aware(datetime(datetime.now().year, 5, 1)), timezone.make_aware(datetime(datetime.now().year, 5, 31))),
        'Jun': (timezone.make_aware(datetime(datetime.now().year, 6, 1)), timezone.make_aware(datetime(datetime.now().year, 6, 30))),
        'Jul': (timezone.make_aware(datetime(datetime.now().year, 7, 1)), timezone.make_aware(datetime(datetime.now().year, 7, 31))),
        'Ago': (timezone.make_aware(datetime(datetime.now().year, 8, 1)), timezone.make_aware(datetime(datetime.now().year, 8, 31))),
        'Set': (timezone.make_aware(datetime(datetime.now().year, 9, 1)), timezone.make_aware(datetime(datetime.now().year, 9, 30))),
        'Out': (timezone.make_aware(datetime(datetime.now().year, 10, 1)), timezone.make_aware(datetime(datetime.now().year, 10, 31))),
        'Nov': (timezone.make_aware(datetime(datetime.now().year, 11, 1)), timezone.make_aware(datetime(datetime.now().year, 11, 30))),
        'Dez': (timezone.make_aware(datetime(datetime.now().year, 12, 1)), timezone.make_aware(datetime(datetime.now().year, 12, 31))),
    }

    # Inicializar o dicionário de valores totais por mês
    valores_totais = []

    # Somar o total de vendas para cada mês
    for mes, (inicio, fim) in intervalo_meses.items():
        valor_total = (
            Venda.objects.filter(data_venda__gte=inicio, data_venda__lte=fim)
            .aggregate(total=Sum('valor_total'))['total']
        )
        # Adicionar o valor (ou 0 se não houver vendas)
        valores_totais.append(valor_total or 0)

    # Preparar os dados do gráfico
    meses = list(intervalo_meses.keys())

    # Plotar o gráfico
    plt.figure(figsize=(10, 6))
    plt.bar(meses, valores_totais, color='blue')
    plt.xlabel('Mês')
    plt.ylabel('Total de Vendas (R$)')
    plt.title('Vendas Mensais')
    plt.tight_layout()

    # Gerar a imagem para exibição no template
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Converter a imagem para Base64 para o template
    graphic = base64.b64encode(image_png).decode('utf-8')
    plt.close()

    return render(request, 'grafico_mes.html', {'graphic': graphic, 'erro': None})

def grafico_diario(request):
    # Agrupar por dia e calcular soma de vendas e contagem de vendas
    vendas_dia = (
        Venda.objects.annotate(dia=TruncDay('data_venda'))
        .values('dia')
        .annotate(valor_total=Sum('valor_total'), quantidade=Count('id'))
        .order_by('dia')
    )

    dias = [venda['dia'].strftime('%Y-%m-%d') for venda in vendas_dia]
    valores_totais = [venda['valor_total'] for venda in vendas_dia]

    # Plotar os gráficos usando Matplotlib
    plt.figure(figsize=(10, 6))
    plt.bar(dias, valores_totais, color='purple', alpha=0.7, label='Valor Total (R$)')

    plt.xlabel('Dia')
    plt.ylabel('Valores')
    plt.title('Vendas Diárias')
    plt.xticks(rotation=25)
    plt.legend()

    # Gerar a imagem para exibição no template
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Converter a imagem para Base64 para o template
    graphic = base64.b64encode(image_png).decode('utf-8')
    plt.close()

    return render(request, 'grafico_diario.html', {'graphic': graphic})
