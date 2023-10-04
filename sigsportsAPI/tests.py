from sigsportsAPI.models import Matricula, Modalidade
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient

class ModalidadeTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.data = {
            "nomeModalidade": "Futebol",
            "descricao": "jogo de futebol"
        }


    # Teste de consultado ao banco de dados com objeto de modalidade
    def test_create_modalidade(self):
        response = self.client.post('/api/v1/criarModalidade', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Consulta ao banco de dados
        modalidade = Modalidade.objects.get(nomeModalidade=self.data['nomeModalidade'])
        self.assertIsNotNone(modalidade)
        self.assertEqual(modalidade.descricao, self.data['descricao'])

    # Dados inválidos
    def test_create_modalidade_with_invalid_data(self):
        data = {
            "nomeModalidade": "",
            "descricao": "jogo de futebol"
        }
        response = self.client.post('/api/v1/criarModalidade', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
