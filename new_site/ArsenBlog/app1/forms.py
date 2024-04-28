from django import forms
from .models import Comment, Post, PostPoint, User

class SearchForm(forms.Form):
    query=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mr-sm-2", "type":"search", "placeholder":"Введіть пошуковий запит", "aria-label":"Search"}), max_length=100)

class UserEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=("first_name", "last_name", "username", "email")


class UserEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=("first_name", "last_name", "username", "email")

class RegistrationForm(forms.ModelForm):
    password=forms.CharField(max_length=8, widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=("first_name", "last_name", "username", "email", "password")

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=("title", "tag", "short_des", "img")

class PostPointForm(forms.ModelForm):
    class Meta:
        model=PostPoint
        fields=("header", "post_point_text", "post_img")


class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=("name", "emeil", "text")

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"id": "username", "class":"form-control", "placeholder": "Введть логін"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"id": "password", "class":"form-control", "placeholder": "Введть пароль"}))