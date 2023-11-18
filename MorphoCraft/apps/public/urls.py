from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "public"
urlpatterns = [
    #Pages
    path("", views.index, name="store"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:user_username>", views.profile, name="profile"),
    path("profile/<str:user_username>/update", views.update_profile, name="update_profile"),
    path("profile/<str:user_username>/update_password", views.change_password, name="change_password"),
    path("product/create/", views.create_product, name="product_creation"),
    path("product",views.product, name="product"),
    path("product/table",views.table, name="table"),
    path("product/chair",views.chair, name="chair"),
    path("product/manage", views.product_management, name="product_management"),
    path("order_history",views.order_history, name="order_history"),
    path("review",views.review_page, name="review_page"),
    path("product/submit_review/<int:product_id>", views.submit_review, name="submit_review"),
    path("cart", views.cart, name="cart"),
    path("checkout",views.checkout, name="checkout"),
    path("password_reset/", views.CustomPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    #Funtions
    path("get_data/", views.get_data, name="get_data"),
    path("update_item/", views.updateItem, name="update_item"),
    path("process_order/", views.processOrder, name="process_order"),
    path("get_reviews/", views.get_reviews, name="get_reviews"),
    
    path("update_product/<int:product_id>/", views.update_product, name="update_product"),
    path("delete_product/<int:product_id>/", views.delete_product, name="delete_product"),
    path("delete_account/", views.delete_account, name="delete_account"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
]