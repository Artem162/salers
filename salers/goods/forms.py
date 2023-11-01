from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

from .models import *


# ————————————————————————————————————————————————————————————————————————————————————————————————————————————
# Community forms:
class SellForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Category is not selected"

    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['title', 'slug', 'description', 'photo', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input',
                                            'placeholder': 'Product name'
                                            }),

            'slug': forms.TextInput(attrs={'class': 'form-input',
                                           'placeholder': 'Product slug'
                                           }),

            'description': forms.Textarea(attrs={'cols': 10, 'rows': 3, 'class': 'form-input',
                                                 'placeholder': 'description of the product'
                                                 }),

        }


class FeedbackForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input',
                                                         'placeholder': 'enter your name'
                                                         }))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-input',
                                                           'placeholder': 'enter your email'}))

    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 3, 'class': 'form-input',
                                                           'placeholder': 'enter your message'}))

    captcha = CaptchaField()




# ————————————————————————————————————————————————————————————————————————————————————————————————————————————
# Registration forms:
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input',
                                                             'placeholder': 'enter your username'}))

    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-input',
                                                           'placeholder': 'enter your Email'}))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input',
                                                                  'placeholder': 'enter your password'}))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input',
                                                                  'placeholder': 'repeat your password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login:', widget=forms.TextInput(attrs={'class': 'form-input',
                                                                             'placeholder': 'enter your username'}))
    password = forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={'class': 'form-input',
                                                                                    'placeholder': 'enter your password'
                                                                                    }))
# ————————————————————————————————————————————————————————————————————————————————————————————————————————————
