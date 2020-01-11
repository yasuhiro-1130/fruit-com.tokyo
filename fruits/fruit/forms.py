from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, \
	 UserCreationForm, UserChangeForm, PasswordChangeForm,\
	 PasswordResetForm, SetPasswordForm
from .models import *
from django.core.exceptions import ValidationError


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['class'] = 'signin-input'


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MyPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MySetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email


class UserEditForm(UserChangeForm):
    class Meta:
         model = User
         exclude = ('email', 'is_staff', 'is_active', 'date_joined',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['postal_code2'].widget.attrs[
            'onKeyUp'] = "AjaxZip3.zip2addr('postal_code1','postal_code2','address1','address2');"


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('user', 'product')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
        self.fields['rating'].widget.attrs['style'] = 'display:none'


class FarmInfoRegisterChangeForm(forms.ModelForm):
    class Meta:
        model = Farm
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            pass

class FarmProductRegisterAndChangeForm(forms.ModelForm):
    class Meta:
        model = FarmProduct
        exclude = ('farm',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class CartItemAmountRegisterAndChangeForm(forms.ModelForm):
    class Meta:
        model = ShoppingCartItem
        fields = ('amount',)
