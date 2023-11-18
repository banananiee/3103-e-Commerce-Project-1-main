import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

from dotenv import load_dotenv
import os

load_dotenv()

# Create your forms here.

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        
    error_messages = {
        "password_req_fail": ('''Password requirements not met.
                                  Password must be at least 8 characters long, 
                                  1 uppercase letter, 1 lowercase letter and 1 digit'''),
        "username_incorrect": ("Username exists or invalid characters used. Only alphanumeric characters are allowed."),
        "password_mismatch": ("The two password fields didn’t match."),
    }
    
    def clean_username(self):
        cleaned_username = self.cleaned_data.get("username").strip()
        check_username = re.search("^[A-Za-z\d_]+$", cleaned_username)

        if check_username is None:
            raise ValidationError(
                self.error_messages["username_incorrect"],
                code="username_incorrect",
            )

        return cleaned_username
    
    def clean_password1(self):
        cleaned_password1 = self.cleaned_data.get("password1")
        check_pwd_rule = re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$", cleaned_password1)
        
        if check_pwd_rule is None:
            raise ValidationError(
                self.error_messages["password_req_fail"],
                code="password_req_fail",
            )

        return cleaned_password1

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
    # error = "Invalid username or password"

class ProductForm(forms.Form):
    top_color = forms.ModelChoiceField(
        queryset=Product.objects.values_list('top_color', flat=True).distinct(),
        empty_label=None,
    )
    bottom_color = forms.ModelChoiceField(
        queryset=Product.objects.values_list('bottom_color', flat=True).distinct(),
        empty_label=None,
    )
    height = forms.ModelChoiceField(
        queryset=Product.objects.values_list('height', flat=True).distinct(),
        empty_label=None,
    )
    width = forms.ModelChoiceField(
        queryset=Product.objects.values_list('width', flat=True).distinct(),
        empty_label=None,
    )
    length = forms.ModelChoiceField(
        queryset=Product.objects.values_list('length', flat=True).distinct(),
        empty_label=None,
    )

class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class PasswordUpdateForm(PasswordChangeForm):
    password = None  # Remove the password field from the form
    error_messages = {
        "password_mismatch": ("The two password fields didn’t match."),
        "password_req_fail": ('''Password requirements not met.
                                  Password must be at least 8 characters long, 
                                  1 uppercase letter, 1 lowercase letter and 1 digit'''),
        "password_incorrect": ("Your old password was entered incorrectly. Please enter it again."),
    }
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Old password",
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="New password",
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm new password",
    )
    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)  # Adding the reCAPTCHA field here

    
    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        check_pwd_rule = re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$", password1)
        if check_pwd_rule is None:
            raise ValidationError(
                self.error_messages["password_req_fail"],
                code="password_req_fail",
            )
        password_validation.validate_password(password2, self.user)
        return password2

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        Also, this function is overrided to add in the pepper and salt.
        """
        print(self.cleaned_data)
        old_password = os.getenv("SECRET_PEPPER") + self.cleaned_data["old_password"] + self.user.salt
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password
    
class PasswordResetForm(SetPasswordForm):
    password = None  # Remove the password field from the form
    error_messages = {
        "password_mismatch": ("The two password fields didn't match."),
        "password_req_fail": ('''Password requirements not met.
                                  Password must be at least 8 characters long, 
                                  1 uppercase letter, 1 lowercase letter and 1 digit''')
    }

    field_order = ["new_password1", "new_password2"]

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        check_pwd_rule = re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$", password1)
        if check_pwd_rule is None:
            raise ValidationError(
                self.error_messages["password_req_fail"],
                code="password_req_fail",
            )
        password_validation.validate_password(password2, self.user)
        return password2

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'unit_number', 'zipcode']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'type', 'image', 'top_color', 'bottom_color', 'length', 'width', 'height']