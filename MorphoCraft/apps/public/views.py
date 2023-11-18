from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib import messages
from django.http import JsonResponse, Http404, HttpResponse
from django.urls import reverse, reverse_lazy
from MorphoCraft.bcryptpasswordhasher import BCryptPasswordHasher
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.core.exceptions import ValidationError
from .forms import *
from .models import *
import json
import datetime
import secrets
import string
from dotenv import load_dotenv
import os
import re
import html
import requests

load_dotenv()

#For different pages
def index(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user = user, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'cartItems':cartItems}
    return render(request, 'index.html', context)

def product(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user = user, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    context = {'cartItems':cartItems}
    return render(request, 'product.html',context)

def logout(request):
    request.session.clear()
    return redirect("/")

def register(request):
    form = None
    if request.method == "POST":
        form = RegisterForm(request.POST)
        recaptcha_response = request.POST.get('recaptchaResponse')
        if verify_recaptcha(recaptcha_response) == False:
            messages.error(request, 'reCAPTCHA verification failed. Please try again.')
        else:
            if form.is_valid() and (form.cleaned_data["password1"] == form.cleaned_data["password2"]):
                user = form.save(commit=False)
                user.is_active = 0
                user.save()
                send_confirmation_email(request,user)

                print("User created:", user)  # Debugging: Print the created user
                return redirect("/login")
            
            else:
                print("Form errors:", [form.errors])  # Debugging: Print form errors
                print("Form errors:", form['username'].errors)  # Debugging: Print form errors

    if form is None:
        form = RegisterForm()
    return render(request=request, template_name="register.html", context={"form": form})

def send_confirmation_email(request, user):
    token = default_token_generator.make_token(user)
    domain = get_current_site(request).domain
    message = render_to_string('activation_email.html', {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token,
    })
    send_mail(
        'Activate Your Account',
        message,
        'morphocraft.3x03@gmail.com',
        [user.email],
    )

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    # Check if the token is valid
    if user is not None and default_token_generator.check_token(user, token):
        # Activate the user and login
        user.is_active = 1
        user.save()
        # return redirect('login')  # Redirect to login or another page
        return redirect('/login')
    else:
        print("error")
        #return render(request, 'activation_invalid.html')  # Render a failure page or message
        return HttpResponse('invalid')

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        # request.session['user_authenticated'] = False

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            

            try:
                pepper = os.getenv("SECRET_PEPPER")
                salt = str(User.objects.get(username=username).salt)
                user_log = User.objects.get(username=username) # TODO: Fix this ugly code
                password = pepper + password + salt
                user = authenticate(request, username=username, password=password)

                def get_client_ip(request):
                    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                    if x_forwarded_for:
                        ip = x_forwarded_for.split(',')[0]
                    else:
                        ip = request.META.get('REMOTE_ADDR')
                    return ip
                
                if user is not None:
                    log_to_save = Log(user_id=user, ip_address=get_client_ip(request), login_success=True)
                    log_to_save.save()
                    login(request, user)
                    request.session['user_authenticated'] = True
                    request.session['user_id'] = user.id
                    request.session['user_username'] = user.username
                    return redirect("/") 
                else:
                    log_to_save = Log(user_id=user_log, ip_address=get_client_ip(request), login_success=False)
                    log_to_save.save() # TODO: And one line above too
                    messages.error(request,'Invalid username or password')
                    request.session['user_authenticated'] = False
                    print("Invalid username or password")

            except User.DoesNotExist:
                messages.error(request,'Invalid username or password')
                request.session['user_authenticated'] = False
                print("Invalid username or password")
    
    form = LoginForm()
    return render(request, "login.html", {"form": form})

@login_required()
def profile(request, user_username):
    try:
        requested_user = User.objects.get(username=user_username)
    except User.DoesNotExist:
        requested_user = None

    user = request.user
    shipping_address = None

    if request.user.is_authenticated and request.user.username == user_username:
        try:
            # Add shipping address information if available
            shipping_address = ShippingAddress.objects.get(user=requested_user)
        except ShippingAddress.DoesNotExist:
            pass
    else:
        raise Http404
        
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=user, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        user = None
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {
        'cartItems': cartItems,
        'user': requested_user,
        'shipping_address': shipping_address,
    }
    return render(request, 'profile.html', context)

def chair(request):
    selected_type = 'chair'  # Set the default type for this view
    # Filter the queryset for each field based on the selected type
    top_color_choices = Product.objects.filter(type=selected_type).values_list('top_color', flat=True).distinct()
    bottom_color_choices = Product.objects.filter(type=selected_type).values_list('bottom_color', flat=True).distinct()
    height_choices = Product.objects.filter(type=selected_type).values_list('height', flat=True).distinct()
    width_choices = Product.objects.filter(type=selected_type).values_list('width', flat=True).distinct()
    length_choices = Product.objects.filter(type=selected_type).values_list('length', flat=True).distinct()

    form = ProductForm(initial={'type': selected_type})
    form.fields['top_color'].queryset = top_color_choices
    form.fields['bottom_color'].queryset = bottom_color_choices
    form.fields['height'].queryset = height_choices
    form.fields['width'].queryset = width_choices
    form.fields['length'].queryset = length_choices

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user = user, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'cartItems':cartItems,'form': form}

    return render(request, 'chair.html', context)

def table(request):
    selected_type = 'table'  # Set the default type for this view
    # Filter the queryset for each field based on the selected type
    top_color_choices = Product.objects.filter(type=selected_type).values_list('top_color', flat=True).distinct()
    bottom_color_choices = Product.objects.filter(type=selected_type).values_list('bottom_color', flat=True).distinct()
    height_choices = Product.objects.filter(type=selected_type).values_list('height', flat=True).distinct()
    width_choices = Product.objects.filter(type=selected_type).values_list('width', flat=True).distinct()
    length_choices = Product.objects.filter(type=selected_type).values_list('length', flat=True).distinct()

    form = ProductForm(initial={'type': selected_type})
    form.fields['top_color'].queryset = top_color_choices
    form.fields['bottom_color'].queryset = bottom_color_choices
    form.fields['height'].queryset = height_choices
    form.fields['width'].queryset = width_choices
    form.fields['length'].queryset = length_choices

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user = user, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'cartItems':cartItems,'form': form}

    return render(request, 'table.html', context)

@login_required()
def cart(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user = user, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context = {
        'items':items, 
        'order':order, 
        'cartItems':cartItems
        }
    return render(request, 'cart.html',context)

@login_required()
def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user = user, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        try:
            shipping_address = ShippingAddress.objects.get(user=user)
        except ShippingAddress.DoesNotExist:
            shipping_address = None
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context = {'items':items, 'order':order, 'cartItems':cartItems, 'shipping_address': shipping_address}
    return render(request, 'checkout.html', context)

@login_required()
def order_history(request):
    if request.user.is_authenticated:
        user = request.user
        completed_orders = Order.objects.filter(user= user, completed=True).order_by('-date_ordered')
        order, created = Order.objects.get_or_create(user = user, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        completed_orders = []
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    
    context = {
        'completed_orders': completed_orders,
        'cartItems':cartItems
        }
    return render(request, 'order_history.html',context)

def review_page(request):
    products = Product.objects.all()  # Query all products
    reviews = []  # Initialize an empty list to store reviews
    selected_product = None

    # Handle product selection from the dropdown
    if request.method == 'GET' and 'product' in request.GET:
        product_id = request.GET['product']
        selected_product = Product.objects.filter(id=product_id).first()
        if selected_product:
            reviews = Review.objects.filter(product=selected_product)

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user = user, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {
        'products': products,
        'selected_product': selected_product,
        'reviews': reviews,
        'cartItems':cartItems,
    }

    return render(request, 'review_page.html', context)

@login_required()
def submit_review(request, product_id):
    product = Product.objects.get(id=product_id)  # Get the product based on the product_id
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product  # Assign the product
            review.user = request.user  # Assign the current user
            
            # sanitise review text
            review_text = review.text
            encoded_text = html.escape(review_text)
            review.text = encoded_text
            
            review.save()
            
            return redirect('public:review_page')
    else:
        form = ReviewForm()
    
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user = user, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    context = {
        'form': form,
        'product': product,
        'cartItems':cartItems
    }

    return render(request, 'submit_review.html', context) 

def product_management(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        user = request.user
        if request.user.role == "admin" or request.user.role == "owner":
            order, created = Order.objects.get_or_create(user = user, completed=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            # items = []
            # order = {'get_cart_total':0, 'get_cart_items':0}
            # cartItems = order['get_cart_items']
            raise Http404
    else:
        raise Http404

    context = {'products': products,
               'cartItems':cartItems,
    }
    return render(request, 'product_management.html', context)

def create_product(request):
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the new product
            messages.success(request, 'Your product has been added!')
            return redirect('public:product_creation')  # Redirect to the product management page on success
        else:
            print(form.errors)
            return render(request, 'product_creation.html', {'form': form})
    else:
        # GET request: create a new form instance
        form = ProductCreateForm()
    
    if request.user.is_authenticated:
        if request.user.role == "admin" or request.user.role == "owner":
            user = request.user
            order, created = Order.objects.get_or_create(user = user, completed=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            raise Http404
    else:
        raise Http404
        # items = []
        # order = {'get_cart_total':0, 'get_cart_items':0}
        # cartItems = order['get_cart_items']

    context = {'cartItems':cartItems,
               'form': form
    }

    return render(request, 'product_creation.html', context)

@login_required()
def update_profile(request, user_username):
    try:
        requested_user = User.objects.get(username=user_username)
    except User.DoesNotExist:
        requested_user = None

    if requested_user != request.user:
        raise Http404

    user = request.user

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=user)
        shipping_address_form = ShippingAddressForm(request.POST)

        if profile_form.is_valid() and shipping_address_form.is_valid():
            user = profile_form.save()  # Update the user's profile
            # Create or update the user's shipping address
            address_instance, created = ShippingAddress.objects.get_or_create(user=user)
            address_instance.address = shipping_address_form.cleaned_data['address']
            address_instance.unit_number = shipping_address_form.cleaned_data['unit_number']
            address_instance.zipcode = shipping_address_form.cleaned_data['zipcode']
            address_instance.save()
            

            update_session_auth_hash(request, user)
            messages.success(request, 'Your profile has been updated!')
            return redirect(reverse('public:profile', args=[user.username]))

    else:
        profile_form = ProfileUpdateForm(instance=user)
        # Load the user's shipping address if available
        try:
            shipping_address_instance = ShippingAddress.objects.get(user=user)
            shipping_address_form = ShippingAddressForm(instance=shipping_address_instance)
        except ShippingAddress.DoesNotExist:
            shipping_address_form = ShippingAddressForm()

    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=user, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        user = None
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {
        'cartItems': cartItems,
        'user': requested_user,
        'profile_form': profile_form,
        'shipping_address_form': shipping_address_form,
    }
    return render(request, 'update_profile.html', context)

@login_required()
def change_password(request, user_username):
    try:
        requested_user = User.objects.get(username=user_username)
    except User.DoesNotExist:
        raise Http404
        # messages.error(request, 'User does not exist')
        # return redirect('some-view')  # Replace with your view or URL

    if requested_user != request.user:
        raise Http404

    if request.method == 'POST':
        form = PasswordUpdateForm(request.user, request.POST)  
        recaptcha_response = request.POST.get('recaptchaResponse')
        if verify_recaptcha(recaptcha_response) == False:
            messages.error(request, 'reCAPTCHA verification failed. Please try again.')
        else:    
            if form.is_valid(): # This is_valid() function already checks if the password matches.
                new_password1 = form.cleaned_data.get('new_password1')
                new_password2 = form.cleaned_data.get('new_password2')

                # If the old password is correct, and new passwords match, set the new password
                length = 63  # or however long your salts are
                new_salt = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))
                pepper = os.getenv("SECRET_PEPPER")

                hasher = BCryptPasswordHasher()
                new_salted_password = pepper + new_password1 + new_salt
                requested_user.password = hasher.encode(new_salted_password, hasher.salt())
                requested_user.salt = new_salt  # save the new salt
                requested_user.save()

                # Confirm to the user that the update was successful
                messages.success(request, 'Your password was successfully updated!')
            else:
                messages.error(request, 'Please correct the error below.')
                print(2.2)
                print(form.errors)

        
    else:
        form = PasswordUpdateForm(request.user)
        print(1.1)
    
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {
        'form': form,
        'user': requested_user,
        'cartItems': cartItems,
    }
    return render(request, 'change_password.html',context)

#For differernt processes

@login_required()
def updateItem(request):
    try:
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        print('Action:', action)
        print('Product:', productId)
        user = request.user
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(user = user, completed=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)
        orderItem.save()
        if orderItem.quantity <= 0:
            orderItem.delete()

        return JsonResponse('Item was added', safe=False)
    except:
        raise Http404
    
def get_data(request):
    top_color = request.GET.get('top_color')
    bottom_color = request.GET.get('bottom_color')
    height = request.GET.get('height')
    width = request.GET.get('width')
    length = request.GET.get('length')
    type = request.GET.get('type')

    try:
        product = Product.objects.get(top_color=top_color, bottom_color=bottom_color, height=height, width=width, length=length, type=type)
        unit_price = product.price  # Replace with the actual field name for price in your model
        image_url = product.image.url  # Get the image URL from the database

        response_data = {
            'image_url': image_url,
            'unit_price': unit_price,
            'product_id': product.id,
        }
        print(f"Price sent to client: {unit_price}")

        return JsonResponse(response_data)
    except Product.DoesNotExist:
        # return JsonResponse({'error': 'Product not found'}, status=404)
        raise Http404

@login_required()
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user = user, completed=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.completed = True
        order.save()

        shipping_address = ShippingAddress.objects.filter(user=user).first()

        if not shipping_address:
            # Create a new shipping address if it doesn't exist
            ShippingAddress.objects.create(
                user=user,
                order=order,
                address=data['shipping']['address'],
                unit_number=data['shipping']['unit_number'],
                zipcode=data['shipping']['zipcode'],
            )
            
    else:
        print('User is not logged in..')

    return JsonResponse('Payment submitted..', safe=False)

def get_reviews(request):
    if request.method == 'GET':
        product_id = request.GET.get('product_id')
        reviews = Review.objects.filter(product_id=product_id)
        review_list = []
        if reviews:
            for review in reviews:
                review_list.append({
                    'author': review.user.username,
                    'text': review.text,
                })
            return JsonResponse(review_list, safe=False)

    # Handle other cases, possibly with an error response
    # return JsonResponse({'error': 'Invalid request'}, status=400)
    raise Http404

def update_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST' and (request.user.role == "admin" or request.user.role == "owner"):
        product = Product.objects.get(id=product_id)
        # Update the product fields based on the form data
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.type = request.POST.get('type')
        product.top_color = request.POST.get('top_color')
        product.bottom_color = request.POST.get('bottom_color')
        product.height = request.POST.get('height')
        product.width = request.POST.get('width')
        product.length = request.POST.get('length')
        new_image = request.FILES.get('new_image')  # Get the new image file
        if new_image:
            product.image = new_image 

        product.save()  # Save the updated product
        messages.success(request, f'{product.name} has been updated!')

        return redirect('public:product_management')
    
    else:
        raise Http404

def delete_product(request, product_id):
    # Get the product from the database
    if request.user.is_authenticated:
        if request.user.role == "admin" or request.user.role == "owner":
            product = Product.objects.get(id=product_id)
            product_name = product.name  # Get the product's name before deleting
            product.delete()
            messages.success(request, f'{product_name} has been deleted!')
            return redirect('public:product_management')
    # except Product.DoesNotExist:
        # pass

    # return redirect('public:product_management')
    raise Http404

def delete_account(request):
    if request.user.is_authenticated:
        # Assuming you want to delete the currently logged-in user
        request.user.delete()
        logout(request)
        return redirect('public:store')
    else:
        raise Http404

def verify_recaptcha(response):
    payload = {
        'secret': settings.RECAPTCHA_PRIVATE_KEY,
        'response': response
    }
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
    result = response.json()
    print(f"Verification Result: {result}")
    return result.get('success')

# modify some values in django.contrib.auth.views
class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy("public:password_reset_done")

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("public:password_reset_complete")
    form_class = PasswordResetForm
    