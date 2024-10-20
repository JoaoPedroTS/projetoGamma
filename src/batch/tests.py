from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Batch
from farm.models import Farm

# Create your tests here.
class BatchModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="a1b2c3",
        )

        self.farm = Farm.objects.create(
            farm_name = "fazendaExemplo",
            farm_owner = "proprietarioExemplo",
            farm_location = "localidadeExemplo"
        )

        self.batch = Batch.objects.create(
            farm = self.farm,
            batch_name = "nomeLote",
            animal_type = "nomeRaca",
            batch_size = 50
        )

    def test_farm_creation(self):
        self.assertEqual(self.batch.farm, self.farm)
        self.assertEqual(self.batch.batch_name, "nomeLote")
        self.assertEqual(self.batch.animal_type, "nomeRaca")
        self.assertEqual(self.batch.batch_size, 50)

class FarmViewTest(TestCase):
    def setUp(self):
        self.farm = Farm.objects.create(
            farm_name = "fazendaExemplo",
            farm_owner = "proprietarioExemplo",
            farm_location = "localidadeExemplo"
        )

        self.batch = Batch.objects.create(
            farm = self.farm,
            batch_name = "nomeLote",
            animal_type = "nomeRaca",
            batch_size = 50
        )

    def test_batch_index_status_code(self):
        response = self.client.get(reverse("batch_index"))
        self.assertEqual(response.status_code, 200)
    
    def test_add_batch_status_code(self):
        response = self.client.get(reverse("add_batch"))
        self.assertEqual(response.status_code, 200)
    
    def test_edit_batch_status_code(self):
        response = self.client.get(reverse("edit_batch"))
        self.assertEqual(response.status_code, 200)
    
    def test_delete_batch_status_code(self):
        response = self.client.get(reverse("delete_batch"))
        self.assertEqual(response.status_code, 200)
    
    def test_batch_detail_status_code(self):
        response = self.client.get(reverse("delete_batch", args=[self.batch.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["batch"].batc_name, "nomeLote")
