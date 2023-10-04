from rest_framework import generics, status, serializers
from rest_framework.response import Response
from .models import Matricula, Modalidade, CategoriaModalidade, Professor, Turma, AlunoTurma
from .serializers import MatriculaSerializer, ModalidadeSerializer, CategoriaModalidadeSerializer, ProfessorSerializer, TurmaSerializer, TurmaVagasSerializer
from django.shortcuts import get_object_or_404

#from .pagination import PaginacaoPadrao
# Create your views here.
#teste


# matricula
class FazerMatricula(generics.CreateAPIView):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer

    def perform_create(self, serializer):
        # Obtém o ID da turma do URL
        turma_id = self.kwargs.get('pk')

        # Verifica se a matrícula já existe para a turma especificada
        turma = Turma.objects.get(id=turma_id)
        matricula_numero = serializer.validated_data.get('matricula')
        matricula_existe = Matricula.objects.filter(matricula=matricula_numero, alunoturma__turma=turma).exists()
        if matricula_existe:
            raise serializers.ValidationError({'erro': 'Matrícula já existe para a turma especificada.'})
        else:
            # Cria a matrícula
            matricula = serializer.save()

            # Cria o vínculo entre a matrícula e a turma
            AlunoTurma.objects.create(matricula=matricula, turma=turma)

            return matricula




class ListarMatriculas(generics.ListAPIView):
    #queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer


    def get_queryset(self):
        turma_id = self.kwargs['pk']  # Obtém o ID da turma do URL
        turma = get_object_or_404(Turma, id = turma_id)

        queryset = Matricula.objects.filter(alunoturma__turma = turma)
        return queryset

class GerenciarMatriculaId(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MatriculaSerializer

    def get_object(self):
        matricula_id = self.kwargs['id_matricula']  # Obtém o ID da matrícula do URL

        matricula = get_object_or_404(Matricula, id=matricula_id)

        obj = get_object_or_404(Matricula.objects.filter(alunoturma__matricula=matricula))
        self.check_object_permissions(self.request, obj)

        return obj



# modalidades

class CriarModalidade(generics.CreateAPIView):
    queryset = Modalidade.objects.all()
    serializer_class = ModalidadeSerializer

class ListarModalidades(generics.ListAPIView):
    queryset = Modalidade.objects.all()
    serializer_class = ModalidadeSerializer

class ListarModalidadeId(generics.RetrieveAPIView):
    queryset = Modalidade.objects.all()
    serializer_class = ModalidadeSerializer
    lookup_field = 'id'


# categorias
class CriarCategoria(generics.CreateAPIView):
    queryset = CategoriaModalidade.objects.all()
    serializer_class = CategoriaModalidadeSerializer


class ListarCategorias(generics.ListAPIView):
    queryset = CategoriaModalidade.objects.all()
    serializer_class = CategoriaModalidadeSerializer

class ListarCategoriaId(generics.RetrieveAPIView):
    queryset = CategoriaModalidade.objects.all()
    serializer_class = CategoriaModalidadeSerializer
    lookup_field = 'id'


# professor
class CriarProfessor(generics.CreateAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

class ListarProfessores(generics.ListAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

class ListarProfessorId(generics.RetrieveAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    lookup_field = 'id'


#turmas

class QuantidadeVagasTurma(generics.ListAPIView):
    serializer_class = TurmaVagasSerializer

    def get_queryset(self):
        turmas = Turma.objects.all()
        return turmas

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = []

        for turma in queryset:
            vagas_restantes = turma.vagas - turma.alunoturma_set.count()
            turma_data = {
                'turma_id': turma.id,
                'nome_turma': turma.nomeTurma,
                'vagas_restantes': vagas_restantes
            }
            data.append(turma_data)

        return Response(data)



class QuantidadeVagasTurmaPorId(generics.RetrieveAPIView):
    serializer_class = TurmaVagasSerializer

    def get_queryset(self):
        turma_id = self.kwargs['pk'] # Obtém o ID da turma do URL

        turma = Turma.objects.filter(id = turma_id)
        return turma

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        vagas_restantes = instance.vagas - instance.alunoturma_set.count()
        turma_data = {
            'turma_id': instance.id,
            'nome_turma': instance.nomeTurma,
            'vagas_restantes': vagas_restantes
        }
        return Response(turma_data)



class CriarTurma(generics.CreateAPIView):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        turma = serializer.save()


        response_data = serializer.data
        response_data['modalidade'] = turma.modalidade.nomeModalidade
        response_data['categoria'] = turma.categoria.categoria
        response_data['professor'] = turma.professor.nome
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

class ListarTurmas(generics.ListAPIView):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Percorre cada instância para formatar os campos relacionados
        for index, instance in enumerate(queryset):
            professor = instance.professor
            modalidade = instance.modalidade
            categoria = instance.categoria

            professor_nome = professor.nome  # Substitua 'nome' pelo campo correto do professor
            modalidade_nome = modalidade.nomeModalidade  # Substitua 'nomeModalidade' pelo campo correto da modalidade
            categoria_nome = categoria.categoria  # Substitua 'categoria' pelo campo correto dentro do objeto categoria

            # Atualiza os campos formatados na representação serializada
            serialized_data = serializer.data[index]
            serialized_data['professor'] = professor_nome
            serialized_data['modalidade'] = modalidade_nome
            serialized_data['categoria'] = categoria_nome

        return Response(serializer.data)


class GerenciarTurmaId(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TurmaSerializer

    def get_queryset(self):
        turma_id = self.kwargs['pk']  # Obtém o ID da turma do URL
        return Turma.objects.filter(id=turma_id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Obtém os objetos relacionados
        professor = instance.professor
        modalidade = instance.modalidade
        categoria = instance.categoria

        # Formata os campos relacionados
        professor_nome = professor.nome  # Substitua 'nome' pelo campo correto do professor
        modalidade_nome = modalidade.nomeModalidade  # Substitua 'nomeModalidade' pelo campo correto da modalidade
        categoria_nome = categoria.categoria  # Substitua 'categoria' pelo campo correto dentro do objeto categoria

        # Adiciona os campos formatados à representação serializada
        serialized_data = serializer.data
        serialized_data['professor'] = professor_nome
        serialized_data['modalidade'] = modalidade_nome
        serialized_data['categoria'] = categoria_nome

        return Response(serialized_data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
class ListarTurmasPaginadas(generics.ListAPIView):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer
    pagination_class = PaginacaoPadrao
"""
class ListarTurmasId(generics.ListAPIView):
    serializer_class = TurmaSerializer

    def get_queryset(self):
        professor_matricula = self.kwargs['professor_matricula']  # Obtém o ID do professor do URL
        return Turma.objects.filter(professor=professor_matricula)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Percorre cada instância para formatar os campos relacionados
        for index, instance in enumerate(queryset):
            professor = instance.professor
            modalidade = instance.modalidade
            categoria = instance.categoria

            professor_nome = professor.nome  # Substitua 'nome' pelo campo correto do professor
            modalidade_nome = modalidade.nomeModalidade  # Substitua 'nomeModalidade' pelo campo correto da modalidade
            categoria_nome = categoria.categoria  # Substitua 'categoria' pelo campo correto dentro do objeto categoria

            # Atualiza os campos formatados na representação serializada
            serialized_data = serializer.data[index]
            serialized_data['professor'] = professor_nome
            serialized_data['modalidade'] = modalidade_nome
            serialized_data['categoria'] = categoria_nome

        return Response(serializer.data)
