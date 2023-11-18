from django.test import TestCase, Client
from MorphoCraft.apps.public.models import User
from django.urls import reverse
from unittest import mock
import json
import requests

def verify_recaptcha(response):
    payload = {
        'secret': '6LeBsPUoAAAAAA8N5Id4aVecmaZetzsHB6HPQcBZ',
        'response': response
    }
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
    result = response.json()
    print(f"Verification Result: {result}")
    return result.get('success')

class ReCaptchaTestCaseRegister(TestCase):
    def setUp(self):
        self.client=Client()
        self.recaptcha_patch = mock.patch('MorphoCraft.apps.public.views.verify_recaptcha')
        self.mock_verify = self.recaptcha_patch.start()

    #def test_tear_down(self):
     #   self.recaptcha_patch.stop()

    def test_view_with_valid_recaptcha(self):
        self.mock_verify.return_value = True
        fields = {"username": "TestUser", "email": "testuser@gmail.com","password1": "Qwerty123", "password2": "Qwerty123", 'recaptchaResponse':'test'}
        response = self.client.post('/register', fields, follow=True)
        number_of_users = User.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(number_of_users ,1)
    
    def test_view_with_invalid_recaptcha(self):
        self.mock_verify.return_value = False
        fields = {"username": "TestUser", "email": "testuser@gmail.com","password1": "Qwerty123", "password2": "Qwerty123", 'recaptchaResponse':'test'}
        response = self.client.post('/register', fields, follow=True)
        number_of_users = User.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(number_of_users ,0)

class ReCaptchaTestCaseChangePassword(TestCase):
    def setUp(self):
        self.recaptcha_patch = mock.patch('MorphoCraft.apps.public.views.verify_recaptcha')
        self.mock_verify = self.recaptcha_patch.start()
        self.password = "Just ignore me, not real password1"
        self.user = User.objects.create(username="potato",
                            email="potato@potatoworld.com", 
                            password="bcrypt_sha256$$2b$13$VLLdqaJzaaRzI6wOFVqULe3.b4IvnkKnXG6f.LI7TVVYI4wHcIH8K",
                            salt="WCHkGIFXNmKb0eYn78pSI8PLwI1QVBmuFKZElgGYyFCrEuftfQS6IWj0x6VERA7",
                            role="user")
        self.client = Client()
        self.client.post("/login", {"username": "potato", "password": self.password}, follow=True)

    def test_view_with_valid_recaptcha(self):
        self.mock_verify.return_value = True
        fields = {"old_password": self.password, "new_password1": "Qwerty123", "new_password2": "Qwerty123"} 
        response = self.client.post('/profile/potato/update_password', fields, follow=True)
        password = User.objects.get(username="potato").password
        self.assertNotEqual(password,"bcrypt_sha256$$2b$13$VLLdqaJzaaRzI6wOFVqULe3.b4IvnkKnXG6f.LI7TVVYI4wHcIH8K")

    def test_view_with_invalid_recaptcha(self):
        self.mock_verify.return_value = False
        fields = {"old_password": self.password, "new_password1": "Qwerty123", "new_password2": "Qwerty123"} 
        response = self.client.post('/profile/potato/update_password', fields, follow=True)
        password = User.objects.get(username="potato").password
        self.assertEqual(password,"bcrypt_sha256$$2b$13$VLLdqaJzaaRzI6wOFVqULe3.b4IvnkKnXG6f.LI7TVVYI4wHcIH8K")