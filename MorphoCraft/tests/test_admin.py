from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.urls.exceptions import Resolver404
from MorphoCraft.apps.public.models import User
from MorphoCraft.views import *

class CredentialSetup(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="just_a_user",
                            email="stereotypicaluser@gmail.com",
                            password="bcrypt_sha256$$2b$13$6QR2q8168iLgfnZaLg6XzuuqemUb8jxXQzCBeFowjUl3AWI7DGWIi",
                            salt="I3oD4FWbgNSzmhjQjkM8aVoenqV0VLynSR6ugZLnm5NuTYBSbt2QfvWknL8J4wZ",
                            role="user")
        
        self.owner1 = User.objects.create(username="I_am_an_owner",
                            email="anOwner@gmail.com",
                            password="bcrypt_sha256$$2b$13$f0sT1XN8/F6MDGH17IVoR.jFnKW5vCXobenW4pBA26HExy6RcG5yK",
                            salt="er9bpKbZJYKXdfqiNMTBX0q9ulOCmRMfHZj5W6lv7uTAAO5iDAIGgRFlJefCs1s",
                            role="owner")
        
        self.admin1 = User.objects.create(username="admin",
                            email="admin@therealadmin.com", 
                            password="bcrypt_sha256$$2b$13$VLLdqaJzaaRzI6wOFVqULe3.b4IvnkKnXG6f.LI7TVVYI4wHcIH8K",
                            salt="WCHkGIFXNmKb0eYn78pSI8PLwI1QVBmuFKZElgGYyFCrEuftfQS6IWj0x6VERA7",
                            role="admin")
        
        self.client_public = Client()
        self.client_user = Client()
        self.client_owner = Client()
        self.client_admin = Client()   
        
        self.client_user.post("/login", {"username": "just_a_user", "password": "lmao"}, follow=True)
        self.client_owner.post("/login", {"username": "I_am_an_owner", "password": "Nah, nothing much, not relevant"}, follow=True)
        self.client_admin.post("/login", {"username": "admin", "password": "Just ignore me, not real password1"}, follow=True)

class AdminAccessTest(CredentialSetup):

    def test_url_resolve(self):
        url = reverse("admin")
        self.assertEqual(resolve(url).func, admin_index)
        self.assertEqual(resolve("/admin").func, admin_index)
        self.assertEqual(resolve("/admin/").func, admin_index)
        self.assertEqual(resolve("/admin/home").func, admin_index)
    
    def test_url_access(self):
        response_public = self.client_public.get(reverse("admin"))
        response_user = self.client_user.get(reverse("admin"))
        response_owner = self.client_owner.get(reverse("admin"))
        response_admin = self.client_admin.get(reverse("admin"))

        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

class AdminUserTestCase(CredentialSetup):
    def setUp(self):
        super().setUp()
        self.user2 = User.objects.create(username="new_user_here",
                            email="newuser@gmail.com",
                            password="bcrypt_sha256$$2b$13$6QR2q8168iLgfnZaLg6XzuuqemUb8jxXQzCBeFowjUl3AWI7DGWIi",
                            salt="I3oD4FWbgNSzmhjQjkM8aVoenqV0VLynSR6ugZLnm5NuTYBSbt2QfvWknL8J4wZ",
                            role="user")


    def test_url_resolve(self):
        url = reverse("admin_users")
        self.assertEqual(resolve(url).func, admin_users)
        self.assertEqual(resolve("/admin/users").func, admin_users)
        self.assertEqual(resolve("/admin/users/action=search").func, admin_users)
        self.assertEqual(resolve("/admin/users/action=update").func, admin_users)
        self.assertEqual(resolve("/admin/users/action=delete").func, admin_users)
        self.assertEqual(resolve("/admin/users/action=wtv").func, admin_users)
    

    def test_url_access(self):
        # Test reverse
        response_public = self.client_public.get(reverse("admin_users"))
        response_user = self.client_user.get(reverse("admin_users"))
        response_owner = self.client_owner.get(reverse("admin_users"))
        response_admin = self.client_admin.get(reverse("admin_users"))    

        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

        # test user search access
        response_public = self.client_public.get("/admin/users/action=search")
        response_user = self.client_user.get("/admin/users/action=search")
        response_owner = self.client_owner.get("/admin/users/action=search")
        response_admin = self.client_admin.get("/admin/users/action=search")
        
        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

        # test user update access
        response_public = self.client_public.get("/admin/users/action=update")
        response_user = self.client_user.get("/admin/users/action=update")
        response_owner = self.client_owner.get("/admin/users/action=update")
        response_admin = self.client_admin.get("/admin/users/action=update")
        
        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

        # test user delete access
        response_public = self.client_public.get("/admin/users/action=delete")
        response_user = self.client_user.get("/admin/users/action=delete")
        response_owner = self.client_owner.get("/admin/users/action=delete")
        response_admin = self.client_admin.get("/admin/users/action=delete")
        
        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

        # test random url in /admin/users access
        response_public = self.client_public.get("/admin/users/what")
        response_user = self.client_user.get("/admin/users/smgthelse")
        response_owner = self.client_owner.get("/admin/users/eh")
        response_admin = self.client_admin.get("/admin/users/doesntexist")

        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 404)

    def test_user_search(self):
        # Test normal user search
        response_admin = self.client_admin.post("/admin/users/action=search", data={"username": "user"})
        user_obj_list = response_admin.context["user_list"]
        username_list = [user.username for user in user_obj_list]

        self.assertEqual(len(user_obj_list), 2)
        self.assertEqual(username_list, [self.user1.username, self.user2.username])
        
        # Test non-existent user
        response_admin = self.client_admin.post("/admin/users/action=search", data={"username": "nonothingexist"})
        user_obj_list = response_admin.context["user_list"]
        username_list = [user.username for user in user_obj_list]

        self.assertEqual(len(user_obj_list), 0)
        self.assertEqual(username_list, [])

        # Test Single User Search
        response_admin = self.client_admin.post("/admin/users/action=search", data={"username": "admi"})
        user_obj_list = response_admin.context["user_list"]
        username_list = [user.username for user in user_obj_list]

        self.assertEqual(len(user_obj_list), 1)
        self.assertEqual(username_list, [self.admin1.username])

        # Test Get All User Search
        response_admin = self.client_admin.post("/admin/users/action=search", data={"username": ""})
        user_obj_list = response_admin.context["user_list"]
        username_list = [user.username for user in user_obj_list]

        self.assertEqual(len(user_obj_list), 4)
        self.assertEqual(username_list, [self.user1.username, self.owner1.username, self.admin1.username, self.user2.username])

    def test_user_update(self):
        # Test normal user update
        update_data = {"id": 1, 
                       "username": "", 
                       "email": "new_one@gmail.com", 
                       "verified": "", 
                       "role": "user"
                    }
        response_admin = self.client_admin.post("/admin/users/action=update", data=update_data)
        user_email = [user.email for user in response_admin.context["user_list"] if user.id == 1][0]
        self.assertEqual(user_email, "new_one@gmail.com")
    
    def test_user_delete(self):
        delete_data = {"id": 4}
        response_admin = self.client_admin.post("/admin/users/action=delete", data=delete_data)
        user_email = [user.email for user in response_admin.context["user_list"] if user.id == 4]
        self.assertEqual(user_email, [])

class AdminLogTestCase(CredentialSetup):

    def test_url_resolve(self):
        url = reverse("admin_logs")
        self.assertEqual(resolve(url).func, admin_logs)
        self.assertEqual(resolve("/admin/logs").func, admin_logs)
    
    def test_url_access(self):
        response_public = self.client_public.get(reverse("admin_logs"))
        response_user = self.client_user.get(reverse("admin_logs"))
        response_owner = self.client_owner.get(reverse("admin_logs"))
        response_admin = self.client_admin.get(reverse("admin_logs"))    

        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

        # test log search access
        response_public = self.client_public.get("/admin/logs/action=search")
        response_user = self.client_user.get("/admin/logs/action=search")
        response_owner = self.client_owner.get("/admin/logs/action=search")
        response_admin = self.client_admin.get("/admin/logs/action=search")
        
        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

        # test log update access
        response_public = self.client_public.get("/admin/logs/action=update")
        response_user = self.client_user.get("/admin/logs/action=update")
        response_owner = self.client_owner.get("/admin/logs/action=update")
        response_admin = self.client_admin.get("/admin/logs/action=update")
        
        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

        # test random url in /admin/logs access
        response_public = self.client_public.get("/admin/logs/what")
        response_user = self.client_user.get("/admin/logs/smgthelse")
        response_owner = self.client_owner.get("/admin/logs/eh")
        response_admin = self.client_admin.get("/admin/logs/doesntexist")

        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 404)
    
    def test_log_search(self):
        update_data = {"user_id": 1}
        response_admin = self.client_admin.post("/admin/logs/action=search", data=update_data)
        log_list = [log for log in response_admin.context["log_list"]]
        self.assertEqual(len(log_list), 1)

    def test_log_update(self):
        update_data = {"id": 1, 
                       "details": "This is a new log!"
                    }
        response_admin = self.client_admin.post("/admin/logs/action=update", data=update_data)
        log_details = [log.details for log in response_admin.context["log_list"] if log.log_id == 1][0]
        self.assertEqual(log_details, "This is a new log!")

class AdminReviewTestCase(CredentialSetup):
    def test_url_resolve(self):
        url = reverse("admin_reviews")
        self.assertEqual(resolve(url).func, admin_reviews)
        self.assertEqual(resolve("/admin/reviews").func, admin_reviews)
    
    def test_url_access(self):
        response_public = self.client_public.get(reverse("admin_reviews"))
        response_user = self.client_user.get(reverse("admin_reviews"))
        response_owner = self.client_owner.get(reverse("admin_reviews"))
        response_admin = self.client_admin.get(reverse("admin_reviews"))    

        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

        # test reviews search access
        response_public = self.client_public.get("/admin/reviews/action=search")
        response_user = self.client_user.get("/admin/reviews/action=search")
        response_owner = self.client_owner.get("/admin/reviews/action=search")
        response_admin = self.client_admin.get("/admin/reviews/action=search")
        
        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

        # test reviews update access
        response_public = self.client_public.get("/admin/reviews/action=update")
        response_user = self.client_user.get("/admin/reviews/action=update")
        response_owner = self.client_owner.get("/admin/reviews/action=update")
        response_admin = self.client_admin.get("/admin/reviews/action=update")
        
        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

        # test reviews delete access
        response_public = self.client_public.get("/admin/reviews/action=delete")
        response_user = self.client_user.get("/admin/reviews/action=delete")
        response_owner = self.client_owner.get("/admin/reviews/action=delete")
        response_admin = self.client_admin.get("/admin/reviews/action=delete")
        
        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

        # test random url in /admin/reviews access
        response_public = self.client_public.get("/admin/reviews/what")
        response_user = self.client_user.get("/admin/reviews/smgthelse")
        response_owner = self.client_owner.get("/admin/reviews/eh")
        response_admin = self.client_admin.get("/admin/reviews/doesntexist")

        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 404)

class AdminOrderTestCase(CredentialSetup):
    
    def test_url_resolve(self):
        url = reverse("admin_orders")
        self.assertEqual(resolve(url).func, admin_orders)
        self.assertEqual(resolve("/admin/orders").func, admin_orders)
    
    def test_url_access(self):
        response_public = self.client_public.get(reverse("admin_orders"))
        response_user = self.client_user.get(reverse("admin_orders"))
        response_owner = self.client_owner.get(reverse("admin_orders"))
        response_admin = self.client_admin.get(reverse("admin_orders"))    

        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

        # test orders search access
        response_public = self.client_public.get("/admin/orders/action=search")
        response_user = self.client_user.get("/admin/orders/action=search")
        response_owner = self.client_owner.get("/admin/orders/action=search")
        response_admin = self.client_admin.get("/admin/orders/action=search")
        
        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

        # test orders update access
        response_public = self.client_public.get("/admin/orders/action=update")
        response_user = self.client_user.get("/admin/orders/action=update")
        response_owner = self.client_owner.get("/admin/orders/action=update")
        response_admin = self.client_admin.get("/admin/orders/action=update")
        
        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

        # test orders delete access
        response_public = self.client_public.get("/admin/orders/action=delete")
        response_user = self.client_user.get("/admin/orders/action=delete")
        response_owner = self.client_owner.get("/admin/orders/action=delete")
        response_admin = self.client_admin.get("/admin/orders/action=delete")
        
        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

        # test random url in /admin/orders access
        response_public = self.client_public.get("/admin/orders/what")
        response_user = self.client_user.get("/admin/orders/smgthelse")
        response_owner = self.client_owner.get("/admin/orders/eh")
        response_admin = self.client_admin.get("/admin/orders/doesntexist")

        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 404)


class AdminOrderItemTestCase(CredentialSetup):

    def test_url_resolve(self):
        url = reverse("admin_orderitems")
        self.assertEqual(resolve(url).func, admin_orderitems)
        self.assertEqual(resolve("/admin/orderitems").func, admin_orderitems)
    
    def test_url_access(self):
        response_public = self.client_public.get(reverse("admin_orderitems"))
        response_user = self.client_user.get(reverse("admin_orderitems"))
        response_owner = self.client_owner.get(reverse("admin_orderitems"))
        response_admin = self.client_admin.get(reverse("admin_orderitems"))    

        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

        # test orderitems search access
        response_public = self.client_public.get("/admin/orderitems/action=search")
        response_user = self.client_user.get("/admin/orderitems/action=search")
        response_owner = self.client_owner.get("/admin/orderitems/action=search")
        response_admin = self.client_admin.get("/admin/orderitems/action=search")
        
        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

        # test orderitems delete access
        response_public = self.client_public.get("/admin/orderitems/action=delete")
        response_user = self.client_user.get("/admin/orderitems/action=delete")
        response_owner = self.client_owner.get("/admin/orderitems/action=delete")
        response_admin = self.client_admin.get("/admin/orderitems/action=delete")
        
        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

        # test random url in /admin/orderitems access
        response_public = self.client_public.get("/admin/orderitems/what")
        response_user = self.client_user.get("/admin/orderitems/smgthelse")
        response_owner = self.client_owner.get("/admin/orderitems/eh")
        response_admin = self.client_admin.get("/admin/orderitems/doesntexist")

        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 404)


class AdminShippingTestCase(CredentialSetup):

    def test_url_resolve(self):
        url = reverse("admin_shipping")
        self.assertEqual(resolve(url).func, admin_shipping)
        self.assertEqual(resolve("/admin/shipping").func, admin_shipping)
    
    def test_url_access(self):
        response_public = self.client_public.get(reverse("admin_shipping"))
        response_user = self.client_user.get(reverse("admin_shipping"))
        response_owner = self.client_owner.get(reverse("admin_shipping"))
        response_admin = self.client_admin.get(reverse("admin_shipping"))    

        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

        # test shipping search access
        response_public = self.client_public.get("/admin/shipping/action=search")
        response_user = self.client_user.get("/admin/shipping/action=search")
        response_owner = self.client_owner.get("/admin/shipping/action=search")
        response_admin = self.client_admin.get("/admin/shipping/action=search")
        
        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

        # test shipping update access
        response_public = self.client_public.get("/admin/shipping/action=update")
        response_user = self.client_user.get("/admin/shipping/action=update")
        response_owner = self.client_owner.get("/admin/shipping/action=update")
        response_admin = self.client_admin.get("/admin/shipping/action=update")
        
        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 200)

        # test random url in /admin/shipping access
        response_public = self.client_public.get("/admin/shipping/what")
        response_user = self.client_user.get("/admin/shipping/smgthelse")
        response_owner = self.client_owner.get("/admin/shipping/eh")
        response_admin = self.client_admin.get("/admin/shipping/doesntexist")

        self.assertEqual(response_public.status_code, 404)
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_owner.status_code, 404)
        self.assertEqual(response_admin.status_code, 404)