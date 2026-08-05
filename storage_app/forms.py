from django import forms
from .models import File
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User

        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class FileUploadForm(forms.ModelForm):

    class Meta:
        model = File

        fields = ["file"]