from django.db import models

# Create your models here.

class Bolsista(models.Model):
    nome = models.CharField(max_length=40)
    matricula = models.CharField(max_length=40)
    turno = models.CharField(max_length=40)
    email = models.CharField(max_length=35)

class Modalidade(models.Model):
    nomeModalidade = models.CharField(max_length=40)
    descricao = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.nomeModalidade}'

class CategoriaModalidade(models.Model):
    categoria = models.CharField(max_length=40)
    descricao = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.categoria}'


class Matricula(models.Model):
    nomeAluno = models.CharField(max_length=120)
    matricula = models.CharField(max_length=120)
    #modalidade = models.ForeignKey(Modalidade, on_delete = models.CASCADE)
    curso = models.CharField(max_length = 120)
    #tipoCategoria = models.ForeignKey(CategoriaModalidade, on_delete = models.CASCADE, default=0)
    #dataInscricao = models.DateTimeField(auto_now_add=True, blank=True)
    #autorizado = models.BooleanField(default=False)
    contato = models.CharField(max_length = 120)

    def __str__(self):
        return f'{self.id} - {self.nomeAluno}'


class Professor(models.Model):
    nome = models.CharField(max_length=120)
    matricula = models.CharField(max_length=14)
    email = models.EmailField(max_length=30)

    def __str__(self):
        return f'{self.nome}'

class Turma(models.Model):
    nomeTurma = models.CharField(max_length=120, blank=True)
    modalidade = models.ForeignKey(Modalidade, on_delete = models.CASCADE)
    categoria = models.ForeignKey(CategoriaModalidade, on_delete = models.CASCADE, default=0)
    vagas = models.IntegerField(default=0)
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE)
    genero = models.CharField(max_length=120)
    dias = models.CharField(max_length=40, blank=True)
    horarioInicial = models.CharField(max_length=10, blank=True)
    horarioFinal = models.CharField(max_length=10, blank=True)
    turno = models.CharField(max_length=20, blank=True)
    espaco = models.CharField(max_length=120, blank=True)
    def __str__(self):
        return f'{self.nomeTurma}'



class AlunoTurma(models.Model):
    matricula = models.ForeignKey(Matricula, on_delete = models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete = models.CASCADE)



    def __str__(self):
        return f'{self.id} - {self.matricula.nomeAluno} - {self.turma.nomeTurma}'
