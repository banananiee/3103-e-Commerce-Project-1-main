from django.test import TestCase, Client
from django.urls import reverse, resolve
from MorphoCraft.apps.public.models import User, Product
from MorphoCraft.views import *
from django.http import HttpResponse

# make sure that the users are only enter the pages that they are allowed
class DirectoryTraversalTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create(username="admin", #pass admin
                                              email="admin@mail.com",
                                              password="bcrypt_sha256$$2b$13$KQPaaUlNEpMtDpIfeh74uuMy5g74CUGK64dgYJhKh5cIqcA7vFT5m",
                                              salt="2UUsBMGBeUuNK23B42bB3f3ddjhaTLOMUxQcQkd5mxcgqNoED2VSalvjhVdzZkI", 
                                              role="admin")
        self.owner = User.objects.create(username="owner", #pass 123
                                         email="owner@mail.com",
                                         password="bcrypt_sha256$$2b$13$IaP4Ib8Am7n/HgC0GxcXrOIQvop8R9357FnVYNHmRZE7bBS5zQhHa", 
                                         salt="Mg5vXVQPKigTOpn6j8xR9hQv4g6zMNACvIQSqTuD6icTp0yN0VjtbL8b2ralGys",
                                         role="owner")
        self.user = User.objects.create(username="user", #pass user
                                        email="user@mail.com",
                                        password="bcrypt_sha256$$2b$13$FtHxx/jAPgsnsoLF4GMImusnMk0JO2K/LYpbLaTzeX16W2G9yQnEe", 
                                        salt="WbzW8xCU0y4C3Cyv2s5C7vjKbhBXTn7KzrNfFVJyibew1OhzO5zwoCFRpyX6Nn8",
                                        role="user")

        self.item = Product.objects.create(name="item",
                                           description="this ia a test item",
                                           price="100",
                                           type="table",
                                           image="item.png",
                                           top_color="black",
                                           bottom_color="black",
                                           length="10",
                                           width="10",
                                           height="10")

    def url_test(self, username, password, urlList, statuscode):
        self.client = Client()
        if username != None and password != None:
            self.client.post("/login", {"username": username, "password": password})
        
            logged_in_user = User.objects.get(username=username)
            print("Username:"+logged_in_user.username+" Role:"+logged_in_user.role)
        else:
            print("Username: None Role: None")

        public_urls = [
            reverse("public:store"),
            reverse("public:product"),
            reverse("public:table"),
            reverse("public:chair"),
            reverse("public:review_page"),
            reverse("public:login"),
            reverse("public:register"),
            reverse("public:password_reset")
        ]

        user_urls = [
            reverse("public:update_profile", kwargs={"user_username": username}),
            reverse("public:change_password", kwargs={"user_username": username}),
            reverse("public:submit_review", kwargs={"product_id": 1}),
            reverse("public:order_history"),
            reverse("public:cart")
        ]

        owner_urls = [
            reverse("public:product_management"),
            reverse("public:product_creation"),
        ]

        if urlList == "public":
            urlList = public_urls
        elif urlList == "user":
            urlList = user_urls
        elif urlList == "owner":
            urlList = owner_urls
        else:
            return

        for url in urlList:
            response = self.client.get(url)
            self.assertEqual(response.status_code, statuscode)
    
    def test_public(self):
        # non login users (public)
        self.url_test(None, None, "public", 200)
        # redirects to login
        self.url_test(None, None, "user", 302)
        # no access
        self.url_test(None, None, "owner", 404)

    def test_user(self):
        # user should not be able to access owner urls
        self.url_test("user", "user", "public", 200)
        self.url_test("user", "user", "user", 200)
        # no access
        self.url_test("user", "user", "owner", 404)

    def test_owner(self):
        # owner should be able to access all urls
        self.url_test("owner", "123", "public", 200)
        self.url_test("owner", "123", "user", 200)
        self.url_test("owner", "123", "owner", 200)