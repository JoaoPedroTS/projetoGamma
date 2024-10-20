from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Farm

# Create your tests here.
class FarmModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testUser",
            password="a1b2c3"
        )

        # cria uma fazenda teste
        self.farm = Farm.objects.create(
            farm_name = "NomeFazenda",
            farm_owner = "NomeDono",
            farm_location = "NomeCidade"
        )

    def test_farm_creation(self):
        #Verifica se a fazenda foi criada corretamente
        self.assertEqual(self.farm.farm_name, "NomeFazenda")
        self.assertEqual(self.farm.farm_owner, "NomeDono")
        self.assertEqual(self.farm.farm_location, "NomeCidade")

class FarmViewTest(TestCase):
    def setUp(self):
        # cria uma fazenda teste
        self.farm = Farm.objects.create(
            farm_name = "NomeFazenda",
            farm_owner = "NomeDono",
            farm_location = "NomeCidade"
        )

    def test_farm_index_status_code(self):
        url = reverse("farm_index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_add_farm_status_code(self):
        url = reverse("add_farm")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_edit_farm_status_code(self):
        url = reverse("edit_farm")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_farm_status_code(self):
        url = reverse("delete_farm")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_farm_detail_status_code(self):
        # Testa se a página de detalhe da fazenda responde corretamente
        response = self.client.get(reverse('farm_detail', args=[self.farm.id]))
        
        # Verifica se o status da resposta é 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Verifica se o contexto contém a fazenda correta
        self.assertEqual(response.context['farm'].farm_name, "NomeFazenda")