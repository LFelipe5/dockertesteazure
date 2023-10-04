from rest_framework import serializers

from .models import Matricula, Modalidade, CategoriaModalidade, Professor, Turma, AlunoTurma


class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'nomeAluno', 'matricula', 'contato','curso',)
        model = Matricula

class ModalidadeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'nomeModalidade', 'descricao',)
        model = Modalidade

class CategoriaModalidadeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'categoria', 'descricao',)
        model = CategoriaModalidade

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'nome', 'matricula', 'email')
        model = Professor

class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'nomeTurma','modalidade', 'categoria', 'vagas',
                  'professor', 'genero', 'dias',
                  'horarioInicial', 'horarioFinal', 'turno', 'espaco')
        model = Turma

class AlunoTurmaSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('matricula','turma')
        model = AlunoTurma

class TurmaVagasSerializer(serializers.ModelSerializer):
    vagas_restantes = serializers.SerializerMethodField()

    class Meta:
        model = Turma
        fields = ('id', 'nomeTurma', 'modalidade', 'categoria', 'vagas', 'vagas_restantes')

    def get_vagas_restantes(self, turma):
        return turma.vagas - turma.alunoturma_set.count()
