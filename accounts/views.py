from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django import forms
from .forms import SignUpForm


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')
    success_url = reverse_lazy("home")
    template_name = "registration/signup.html"  
    