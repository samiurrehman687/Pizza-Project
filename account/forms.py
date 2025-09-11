from django import forms
from account.models import Order , CustomerQuery
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
# create forms here


# Registrations Form .....
class RegistrationsForm(forms.ModelForm):
    confirm_password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
        'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-input'}),
        'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-input'}),
        'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-input'}),
        'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-input'}),
        'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-input'}),
        }

    # Match Password ....
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password do not match.")
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'log_input'
        })
    )
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your Password',
            'class': 'log_input'
        })
    )
# order Form ......
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['pizza_name', 'quantity', 'phone_number']  # 'customer' remove
        widgets = {
            'pizza_name': forms.TextInput(attrs={
                'placeholder': 'Pizza Name',
                'class': 'form-input'
            }),
            'quantity': forms.NumberInput(attrs={
                'placeholder': 'Quantity',
                'min': 1,
                'class': 'form-input'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Phone Number',
                'class': 'form-input'
            }),
        }

class CustomerQueryForm(forms.ModelForm):
    class Meta:
        model = CustomerQuery
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your Name',
                'class': 'input-field',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your Email',
                'class': 'input-field',
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'Subject',
                'class': 'input-field'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Message',
                'class': 'input-field'}),
        }