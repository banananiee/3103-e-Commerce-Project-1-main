from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from MorphoCraft.apps.public.models import User, Log, Review, Order, OrderItem, ShippingAddress


class UserSearchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["placeholder"] = "Search username"
        self.fields["username"].widget.attrs["aria-label"] = "Username Search"
        
    class Meta:
        model = User
        fields = ["username"]

class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["id"].widget.attrs["placeholder"] = "Enter User ID"
        self.fields["username"].widget.attrs["placeholder"] = "Enter Username"
        self.fields["username"].required = False
        self.fields["email"].widget.attrs["placeholder"] = "Enter Email"
        self.fields["email"].required = False
        

        for visible in self.visible_fields()[:-1]:
            visible.field.widget.attrs["class"] = "form-control"

    id = forms.IntegerField(min_value=1)
    verified = forms.ChoiceField(choices=[("", None), ("True", True), ("False", False)], required=False)

    class Meta:
        model = User
        fields = ["username", "email", "role"]

class UserDeleteForm(forms.Form):
    id = forms.IntegerField(min_value=1, required=True)

class LogSearchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["user_id"].widget.attrs["placeholder"] = "Search username"
        self.fields["user_id"].widget.attrs["aria-label"] = "Username Search"
        # self.fields["user_id"].required = False
        
    class Meta:
        model = Log
        fields = ["user_id"]

class LogDetailUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["id"].widget.attrs["placeholder"] = "Enter Log ID"
        self.fields["details"].widget.attrs["placeholder"] = "Enter details here..."

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    id = forms.IntegerField(min_value=1)
    
    class Meta:
        model = Log
        fields = ["details"]
    
class ReviewSearchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["user"].widget.attrs["placeholder"] = "Search username"
        self.fields["user"].widget.attrs["aria-label"] = "Username Search"
        # self.fields["user"].required = False
        
    class Meta:
        model = Review
        fields = ["user"]

class ReviewUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["id"].widget.attrs["placeholder"] = "Enter Review ID"
        self.fields["text"].widget.attrs["placeholder"] = "Enter Review to edit"

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    id = forms.IntegerField(min_value=1)

    class Meta:
        model = Review
        fields = ["text"]

class ReviewDeleteForm(forms.Form):
    id = forms.IntegerField(min_value=1, required=True)

class OrderSearchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["user"].widget.attrs["placeholder"] = "Search username"
        self.fields["user"].widget.attrs["aria-label"] = "Username Search"
        # self.fields["user"].required = False
        
    class Meta:
        model = Order
        fields = ["user"]

class OrderUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["completed"].widget.attrs["placeholder"] = "Enter Order ID"
        self.fields["transaction_id"].widget.attrs["placeholder"] = "Enter Transaction ID"

        # for visible in self.visible_fields():
        #     visible.field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Order
        fields = ["completed", "transaction_id"]

    completed = forms.ChoiceField(choices=[("", None), ("True", True), ("False", False)], required=False)
    id = forms.IntegerField(min_value=1)

class OrderDeleteForm(forms.Form):
    id = forms.IntegerField(min_value=1, required=True)

class OrderItemSearchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["product"].widget.attrs["placeholder"] = "Search Product ID"
        self.fields["product"].widget.attrs["aria-label"] = "Product ID Search"
        # self.fields["user"].required = False
        
    class Meta:
        model = OrderItem
        fields = ["product"]

class OrderItemDeleteForm(forms.Form):
    id = forms.IntegerField(min_value=1, required=True)

class ShippingSearchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["user"].widget.attrs["placeholder"] = "Search username"
        self.fields["user"].widget.attrs["aria-label"] = "Username Search"
        # self.fields["user"].required = False
        
    class Meta:
        model = ShippingAddress
        fields = ["user"]

class ShippingUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["id"].widget.attrs["placeholder"] = "Enter Shipping Address ID"
        self.fields["address"].widget.attrs["placeholder"] = "Enter Address"
        self.fields["address"].required = False
        self.fields["unit_number"].widget.attrs["placeholder"] = "Enter Unit Number"
        self.fields["unit_number"].required = False
        self.fields["zipcode"].widget.attrs["placeholder"] = "Enter Zipcode"
        self.fields["zipcode"].required = False
        

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    id = forms.IntegerField(min_value=1)
    class Meta:
        model = ShippingAddress
        fields = ["address", "unit_number", "zipcode"]