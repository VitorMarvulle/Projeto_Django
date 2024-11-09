from django import forms
from app.models import Usuario, Curso, Foto

class FormCadastroUser(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nome','email','senha')
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome', 'class': 'form-control' }),
            'email': forms.EmailInput(attrs={'placeholder': 'usuario@email.com', 'class': 'form-control' }),
            'senha': forms.PasswordInput(attrs={'placeholder': 'Senha', 'class': 'form-control' })
        }

class FormCadastroCurso(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ('nome_curso','autor','duracao', 'preco')
        widgets = {
            'nome_curso': forms.TextInput(attrs={'placeholder': 'Nome do Curso', 'class': 'form-control' }),
            'autor': forms.TextInput(attrs={'placeholder': 'Nome do autor', 'class': 'form-control' }),
            'duracao': forms.NumberInput(attrs={'placeholder': 'Duração em horas', 'class': 'form-control' }),
            'preco': forms.NumberInput(attrs={'step':'0.01', 'placeholder': 'Preço em R$', 'class': 'form-control' }),

        }

class FormLogin(forms.ModelForm):

    class Meta:
        model = Usuario 
        fields = ('email', 'senha')
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'usuario@email.com', 'class': 'form-control' }),
            'senha': forms.PasswordInput(attrs={'class': 'form-control border border-success', 'type': 'password' }),        
            }
        
class FormFoto(forms.ModelForm):
    class Meta:
        model = Foto
        fields = ['nome','foto']

        widgets = {
            'foto': forms.FileInput(attrs={'accept':'image/*'})
        }