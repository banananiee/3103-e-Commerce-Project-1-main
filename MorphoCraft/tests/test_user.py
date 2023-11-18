import os
import secrets
import string
from django.test import TestCase
from django.urls import reverse, resolve
from MorphoCraft.apps.public.models import Product, User, Order, OrderItem
from MorphoCraft.bcryptpasswordhasher import BCryptPasswordHasher


# class OrderCreationTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create(username='testuser', password='testpassword', email='test@example.com')
#         self.product = Product.objects.create(name='Test Product', description='Description', price=100)

#     def test_create_order(self):
#         response = self.client.post('/path/to/order/creation/', {'product_id': self.product.id})
#         self.assertEqual(response.status_code, 200)

#         # Check if the order was created
#         self.assertTrue(Order.objects.filter(user=self.user, completed=False).exists())

#         # Check if the product is associated with the order
#         order = Order.objects.get(user=self.user, completed=False)
#         self.assertTrue(order.orderitem_set.filter(product=self.product).exists())

# class OrderCreationTestCase(TestCase):
#     def setUp(self):
#         # Create a test user
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
        
#         # Create a test product
#         self.product = Product.objects.create(
#             name='Test Product',
#             description='Test Description',
#             price=100.00,
#             type='chair',
#             top_color='red',
#             bottom_color='black',
#             height=50,
#             width=60,
#             length=70,
#         )

#     def test_order_creation(self):
#         # Log in the user
#         self.client.login(username='test', password='Test9230')
    
#         # Add the product to the cart
#         response = self.client.post('/update_item/', {'productId': self.product.id, 'action': 'add'})
#         self.assertEqual(response.status_code, 200)
        
#         # Check if the order was created and contains the correct product
#         order = Order.objects.get(user=self.user, completed=False)
#         self.assertIsNotNone(order)
        
#         order_item = OrderItem.objects.get(order=order, product=self.product)
#         self.assertIsNotNone(order_item)
#         self.assertEqual(order_item.quantity, 1)
        
#         # Submit the order
#         response = self.client.post('/process_order/', {'form': {'total': 100.00}, 'shipping': {'address': '123 Test St', 'unit_number': 'A', 'zipcode': '12345'}})
#         self.assertEqual(response.status_code, 200)
        
#         # Check if the order was completed
#         order.refresh_from_db()
#         self.assertTrue(order.completed)


class LoginTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        length = 63 # Database limit
        def generate_salt(length):
            salt = ''.join(secrets.choice(string.ascii_letters+string.digits) for _ in range(length))
            return salt
        pepper = os.getenv("SECRET_PEPPER")
        password='Test2_9230'
        salt = generate_salt(length)
        password = pepper + password + salt
        self.user = User.objects.create_user(username='test2', password=password, is_active=True, salt=salt, email = "hgj@gfh.com")

    def test_login(self):
        response = self.client.post(reverse('public:login'), {'username': 'test2', 'password': 'Test2_9230'})
        self.assertTrue(self.client.session['user_authenticated'])  # Check if user is authenticated
        self.assertEqual(response.status_code, 302)  # Successful login should redirect

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('public:login'), {'username': 'test1', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)  # Unsuccessful login should return status code 200
        self.assertFalse(self.client.session['user_authenticated'])  # User should not be authenticated
        self.assertContains(response, 'Invalid username or password')  # Check if error message is displayed