from django import forms
from .models import Post, Group

class PostForm(forms.ModelForm):

    def clean_url(self):
        url = self.cleaned_data['url']
        if Post.objects.filter(url=url).exists():
            raise forms.ValidationError("Запись с такой ссылкой уже существует в базе")
        return url

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
