from django.test import TestCase, Client
from django.urls import reverse, resolve
from MorphoCraft.apps.public.models import User, Order, Review, OrderItem, Product
from MorphoCraft.apps.public.forms import PasswordUpdateForm, RegisterForm

# update password
class TestUpdatePassword(TestCase):
    def setUp(self):
        self.password = "Just ignore me, not real password1"
        self.user = User.objects.create(username="potato",
                            email="potato@potatoworld.com", 
                            password="bcrypt_sha256$$2b$13$VLLdqaJzaaRzI6wOFVqULe3.b4IvnkKnXG6f.LI7TVVYI4wHcIH8K",
                            salt="WCHkGIFXNmKb0eYn78pSI8PLwI1QVBmuFKZElgGYyFCrEuftfQS6IWj0x6VERA7",
                            role="user")
        self.client = Client()
        self.client.post("/login", {"username": "potato", "password": self.password}, follow=True)
        
    def test_newPasswordDiff(self):
        
        fields = {"old_password": self.password, "new_password1": "qwertyu12345", "new_password2": "qwertyu12"}
        
        form = PasswordUpdateForm(user=self.user, data=fields)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_password2'][0], "The two password fields didn’t match.")
        
        print([form.errors])
    
    def test_newPasswordFailReqUpper(self):
        fields = {"old_password": self.password, "new_password1": "qwertyu12", "new_password2": "qwertyu12"} # no uppercase
        form = PasswordUpdateForm(user=self.user, data=fields)
        self.assertFalse(form.is_valid())
        self.assertEqual(" ".join(form.errors['new_password2'][0].split()), "Password requirements not met. Password must be at least 8 characters long, 1 uppercase letter, 1 lowercase letter and 1 digit")
        print([form.errors])
    
    def test_newPasswordFailReqLower(self):
        fields = {"old_password": self.password, "new_password1": "QWERTY12", "new_password2": "QWERTY12"} # no lowercase
        form = PasswordUpdateForm(user=self.user, data=fields)
        self.assertFalse(form.is_valid())
        self.assertEqual(" ".join(form.errors['new_password2'][0].split()), "Password requirements not met. Password must be at least 8 characters long, 1 uppercase letter, 1 lowercase letter and 1 digit")
        print([form.errors])
        
    def test_newPasswordFailReqNum(self):
        fields = {"old_password": self.password, "new_password1": "Qwertyui", "new_password2": "Qwertyui"} # no num
        form = PasswordUpdateForm(user=self.user, data=fields)
        self.assertFalse(form.is_valid())
        self.assertEqual(" ".join(form.errors['new_password2'][0].split()), "Password requirements not met. Password must be at least 8 characters long, 1 uppercase letter, 1 lowercase letter and 1 digit")
        print([form.errors])
        
    def test_oldPasswordWrong(self):
        fields = {"old_password": "HELLo123", "new_password1": "Qwerty123", "new_password2": "Qwerty123"} 
        form = PasswordUpdateForm(user=self.user, data=fields)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['old_password'][0], "Your old password was entered incorrectly. Please enter it again.")
        print([form.errors])
        
    def test_correctCase(self):
        fields = {"old_password": self.password, "new_password1": "Qwerty123", "new_password2": "Qwerty123"} 
        form = PasswordUpdateForm(user=self.user, data=fields)
        self.assertTrue(form.is_valid())
        
    
# review: need buy product then review
class TestSubmitReview(TestCase):
    def setUp(self):
        self.password = "Just ignore me, not real password1"
        self.user = User.objects.create(username="potato",
                            email="potato@potatoworld.com", 
                            password="bcrypt_sha256$$2b$13$VLLdqaJzaaRzI6wOFVqULe3.b4IvnkKnXG6f.LI7TVVYI4wHcIH8K",
                            salt="WCHkGIFXNmKb0eYn78pSI8PLwI1QVBmuFKZElgGYyFCrEuftfQS6IWj0x6VERA7",
                            role="user")
        self.client = Client()
        self.client.post("/login", {"username": "potato", "password": self.password}, follow=True)
        
    def test_review(self):
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=100.00,
            type='chair',
            top_color='red',
            bottom_color='black',
            height=50,
            width=60,
            length=70,
        )
        self.order = Order.objects.create(user=self.user,
                             transaction_id="")
        OrderItem.objects.create(product=self.product,
                                 order=self.order,
                                 quantity=2)
        self.client.post("/product/submit_review/1", {"text":"<script>alert('XSS')</script>"})
        self.assertEqual(Review.objects.get(id=1).text, "&lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;")
        print("review test end")
       
# register check regex 
class TestRegisterRegex(TestCase):
    fields = {"username": "TestUser", "email": "testuser@gmail.com","password1": "Qwerty123", "password2": "Qwerty123"}
    
    # username
    def test_usernameField(self):
        field = self.fields
        field["username"] = "TestUser!"
        form = RegisterForm(data=field)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["username"][0], "Username exists or invalid characters used. Only alphanumeric characters are allowed.")
        print([form.errors["username"][0]])
    
    # password req fail
    def test_passwordReqFail(self):
        field = self.fields
        field["password1"] = "qwerty"
        form = RegisterForm(data=field)
        self.assertFalse(form.is_valid())
        self.assertEqual(" ".join(form.errors["password1"][0].split()), "Password requirements not met. Password must be at least 8 characters long, 1 uppercase letter, 1 lowercase letter and 1 digit")
        print([form.errors])
        field["password1"] = "qwerty123"
        form = RegisterForm(data=field)
        self.assertFalse(form.is_valid())
        self.assertEqual(" ".join(form.errors["password1"][0].split()), "Password requirements not met. Password must be at least 8 characters long, 1 uppercase letter, 1 lowercase letter and 1 digit")
        print([form.errors])
        
    # password not same
    def test_passwordDiff(self):
        field = self.fields
        field["password1"] = "Asdfg124"
        form = RegisterForm(data=field)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password2"][0], "The two password fields didn’t match.")
        print([form.errors["password2"][0]])
    
    # correct register test
    def test_RegisterPass(self):
        form = RegisterForm(data=self.fields)
        self.assertTrue(form.is_valid())
        print([form.errors])