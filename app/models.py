from django.db import models

# Create your models here.

class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='imagens/')

class Curso(models.Model):
    nome_curso = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    duracao = models.IntegerField()
    preco = models.DecimalField(max_digits=10,decimal_places=2)
    foto = models.ImageField(upload_to='imagens/')
    estoque = models.CharField(max_length=255)

class Foto(models.Model):
    nome = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='imagens/')

class Contato(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mensagem = models.TextField(max_length=400)
