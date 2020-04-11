from django import forms
from .models import Post, Group

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description", "url", "group", "language"]
        widgets = {
            "group": forms.SelectMultiple(attrs={"size": 3})
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["title", "description"]
