from django.urls import path
#from .views import ListarModalidades, ListarCategorias, FazerMatricula
from . import views
app_name = 'sigsportsAPI'



urlpatterns = [

    path('criarMatricula/<int:pk>', views.FazerMatricula.as_view()),
    path('listarMatriculas/<int:pk>', views.ListarMatriculas.as_view()),
    path('matriculas/<int:id_matricula>', views.GerenciarMatriculaId.as_view(), name='gerenciar-matricula'),
    path('criarModalidade', views.CriarModalidade.as_view()),
    path('listarModalidades', views.ListarModalidades.as_view()),
    path('listarModalidade/<int:id>', views.ListarModalidadeId.as_view()),
    path('criarCategoria', views.CriarCategoria.as_view()),
    path('listarCategorias/', views.ListarCategorias.as_view()),
    path('listarCategorias/<int:id>/', views.ListarCategoriaId.as_view()),
    path('criarProfessor/', views.CriarProfessor.as_view()),
    path('listarProfessores/', views.ListarProfessores.as_view()),
    path('listarProfessor/<int:id>', views.ListarProfessorId.as_view()),
    path('CriarTurma/', views.CriarTurma.as_view()),
    path('listarTurmas/', views.ListarTurmas.as_view()),
    path('vagasDeTurmas', views.QuantidadeVagasTurma.as_view()),
    path('vagasDeTurmas/<int:pk>', views.QuantidadeVagasTurmaPorId.as_view()),
    path('listarTurmasId/<int:professor_matricula>/', views.ListarTurmasId.as_view(), name='listar-turmas-professor'),
    path('gerenciarTurmaId/<int:pk>/', views.GerenciarTurmaId.as_view(), name = 'recuperar-alterar-excluir-turma'),
]

