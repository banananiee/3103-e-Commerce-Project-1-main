from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from MorphoCraft.apps.public.models import User, Log, Review, OrderItem
from MorphoCraft.forms import *
from django.shortcuts import render
from django.http import Http404


def admin_index(request):
    if not request.user.is_authenticated:
        raise Http404
    if request.user.role != "admin":
        raise Http404
    
    return render(request, "admin/admin.html")

def admin_users(request, action=None):
    if not request.user.is_authenticated:
        raise Http404
    if request.user.role != "admin":
        raise Http404
    
    user_list = None
    action_message = ""

    if request.method == "POST":
        if action == "search":
            search_form = UserSearchForm(request.POST)
            if search_form.is_valid():
                username = search_form.cleaned_data["username"]
                user_list = User.objects.filter(username__icontains=username)

        elif action == "update":
            update_form = UserUpdateForm(request.POST)
            if update_form.is_valid():
                user_id = update_form.cleaned_data["id"]
                user = User.objects.get(id=user_id)

                username_updated = update_form.cleaned_data["username"]
                email_updated = update_form.cleaned_data["email"]
                role_updated = update_form.cleaned_data["role"]
                verified_updated = update_form.cleaned_data["verified"]

                # TODO: Find a good way to for loop this easily
                if username_updated not in [None, ""]:
                    if User.objects.filter(username=username_updated).first() is None:
                        user.username = username_updated
                if email_updated not in [None, ""]:
                    if User.objects.filter(email=email_updated).first() is None:
                        user.email = email_updated
                if role_updated not in [None, ""]:
                    user.role = role_updated
                if verified_updated not in [None, ""]:
                    user.verified = verified_updated
                
                user.save()
                action_message += f"User ID {user_id} is updated!<br>"

        elif action == "delete":
            delete_form = UserDeleteForm(request.POST)
            if delete_form.is_valid():  
                user_id = delete_form.cleaned_data["id"]
                if User.objects.filter(id=user_id).first() is None:
                    action_message += f"User ID {user_id} not found.<br>"
                else:
                    User.objects.get(id=user_id).delete()
                    action_message += f"User ID {user_id} is deleted!<br>"
                                 
    if user_list == None:
        user_list = User.objects.all()
    
    if action_message != "":
        action_message = f"<script type='text/javascript'>alert('{action_message}');</script>"
        
    context = {"user_list": user_list,
               "user_search_form": UserSearchForm(),
               "user_update_form": UserUpdateForm(),
               "user_delete_form": UserDeleteForm(),
               "action_message": action_message}
    
    return render(request, "admin/admin_users.html", context)

def admin_logs(request, action=None):
    if not request.user.is_authenticated:
        raise Http404
    if request.user.role != "admin":
        raise Http404
    
    log_list = None
    action_message = ""

    if request.method == "POST":
        if action == "search":
            search_form = LogSearchForm(request.POST)
            if search_form.is_valid():
                username = search_form.cleaned_data["user_id"]
                log_list = Log.objects.filter(user_id__username__icontains=username)
            
        elif action == "update":
            update_form = LogDetailUpdateForm(request.POST)
            if update_form.is_valid():
                log_id = update_form.cleaned_data["id"]
                log = Log.objects.get(log_id=log_id)

                details_update = update_form.cleaned_data["details"]
                if details_update not in [None, ""]:
                    log.details = details_update
                
                log.save()
                action_message += f"Log ID {log_id} is updated!<br>"
    
    if log_list == None:
        log_list = Log.objects.all()
    
    if action_message != "":
        action_message = f"<script type='text/javascript'>alert('{action_message}');</script>"

    context = {"log_list": log_list,
               "log_search_form": LogSearchForm(),
               "log_update_form": LogDetailUpdateForm(),
               "action_message": action_message}

    return render(request, "admin/admin_logs.html", context)

def admin_reviews(request, action=None):
    if not request.user.is_authenticated:
        raise Http404
    if request.user.role != "admin":
        raise Http404
    
    review_list = None
    action_message = ""

    if request.method == "POST":
        if action == "search":
            search_form = ReviewSearchForm(request.POST)
            if search_form.is_valid():
                username = search_form.cleaned_data["user"]
                review_list = Review.objects.filter(user__username__icontains=username)

        elif action == "update":
            update_form = ReviewUpdateForm(request.POST)
            if update_form.is_valid():
                review_id = update_form.cleaned_data["id"]
                review = Review.objects.get(id=review_id)

                review_text_updated = update_form.cleaned_data["text"]
                
                if review_text_updated not in [None, ""]:
                    review.text = review_text_updated

                review.save()

                action_message += f"Review ID {review_id} is updated!<br>"

        elif action == "delete":
            delete_form = ReviewDeleteForm(request.POST)
            if delete_form.is_valid():  
                review_id = delete_form.cleaned_data["id"]
                if Review.objects.filter(id=review_id).first() is None:
                    action_message += f"Review ID {review_id} not found.<br>"
                else:
                    Review.objects.get(id=review_id).delete()
                    action_message += f"Review ID {review_id} is deleted!<br>"
    
    if review_list == None:
        review_list = Review.objects.all()

    context = {"review_list": review_list,
               "review_search_form": ReviewSearchForm(),
               "review_update_form": ReviewUpdateForm(),
               "review_delete_form": ReviewDeleteForm(),
               "action_message": action_message}
    
    return render(request, "admin/admin_reviews.html", context)

def admin_orders(request, action=None):
    if not request.user.is_authenticated:
        raise Http404
    if request.user.role != "admin":
        raise Http404
    
    order_list = None
    action_message = ""

    if request.method == "POST":
        if action == "search":
            search_form = OrderSearchForm(request.POST)
            if search_form.is_valid():
                username = search_form.cleaned_data["user"]
                order_list = Order.objects.filter(user_id__username__icontains=username)
            
        elif action == "update":
            update_form = OrderUpdateForm(request.POST)
            if update_form.is_valid():
                order_id = update_form.cleaned_data["id"]
                order = Order.objects.get(id=order_id)

                transaction_id_update = update_form.cleaned_data["transaction_id"]
                completed_update = update_form.cleaned_data["completed"]

                if transaction_id_update not in [None, ""]:
                    order.transaction_id = transaction_id_update
                if completed_update not in [None, ""]:
                    order.completed = completed_update
                
                order.save()
                action_message += f"Order ID {order_id} is updated!<br>"

        elif action == "delete":
            delete_form = OrderDeleteForm(request.POST)
            if delete_form.is_valid():  
                order_id = delete_form.cleaned_data["id"]
                if Order.objects.filter(id=order_id).first() is None:
                    action_message += f"Order ID {order_id} not found.<br>"
                else:
                    Order.objects.get(id=order_id).delete()
                    action_message += f"Order ID {order_id} is deleted!<br>"
    
    if order_list == None:
        order_list = Order.objects.all()
    
    if action_message != "":
        action_message = f"<script type='text/javascript'>alert('{action_message}');</script>"

    context = {"order_list": order_list,
               "order_search_form": OrderSearchForm(),
               "order_update_form": OrderUpdateForm(),
               "order_delete_form": OrderDeleteForm(),
               "action_message": action_message}
    
    return render(request, "admin/admin_orders.html", context)

def admin_orderitems(request, action=None):
    if not request.user.is_authenticated:
        raise Http404
    if request.user.role != "admin":
        raise Http404
    
    orderitem_list = None
    action_message = ""

    if request.method == "POST":
        if action == "search":
            search_form = OrderItemSearchForm(request.POST)
            if search_form.is_valid():
                product_name = search_form.cleaned_data["product"]
                orderitem_list = OrderItem.objects.filter(product_id__name__icontains=product_name)

        elif action == "delete":
            delete_form = OrderItemDeleteForm(request.POST)
            if delete_form.is_valid():  
                product_id = delete_form.cleaned_data["id"]
                if OrderItem.objects.filter(id=product_id).first() is None:
                    action_message += f"Order Item ID {product_id} not found.<br>"
                else:
                    OrderItem.objects.get(id=product_id).delete()
                    action_message += f"Order Item ID {product_id} is deleted!<br>"
    
    if orderitem_list == None:
        orderitem_list = OrderItem.objects.all()

    context = {"orderitem_list": orderitem_list,
               "orderitem_search_form": OrderItemSearchForm(),
               "orderitem_delete_form": OrderItemDeleteForm(),
               "action_message": action_message}
    
    return render(request, "admin/admin_orderitems.html", context)

def admin_shipping(request, action=None):
    if not request.user.is_authenticated:
        raise Http404
    if request.user.role != "admin":
        raise Http404
    
    shipping_list = None
    action_message = ""

    if request.method == "POST":
        if action == "search":
            search_form = ShippingSearchForm(request.POST)
            if search_form.is_valid():
                username = search_form.cleaned_data["user"]
                shipping_list = ShippingAddress.objects.filter(user_id__username__icontains=username)
            
        elif action == "update":
            update_form = ShippingUpdateForm(request.POST)
            if update_form.is_valid():
                shipping_id = update_form.cleaned_data["id"]
                shipping = ShippingAddress.objects.get(id=shipping_id)

                address_update = update_form.cleaned_data["address"]
                unit_number_update = update_form.cleaned_data["unit_number"]
                zipcode_update = update_form.cleaned_data["zipcode"]

                if address_update not in [None, ""]:
                    shipping.address = address_update
                if unit_number_update not in [None, ""]:
                    shipping.unit_number = unit_number_update
                if zipcode_update not in [None, ""]:
                    shipping.zipcode = zipcode_update
                
                shipping.save()
                action_message += f"Shipping ID {shipping_id} is updated!<br>"
    
    if shipping_list == None:
        shipping_list = ShippingAddress.objects.all()
    
    if action_message != "":
        action_message = f"<script type='text/javascript'>alert('{action_message}');</script>"

    context = {"shipping_list": shipping_list,
               "shipping_search_form": ShippingSearchForm(),
               "shipping_update_form": ShippingUpdateForm(),
               "action_message": action_message}
    
    return render(request, "admin/admin_shipping.html", context)