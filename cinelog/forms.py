from django import forms
from .models import MyModel,Review,Tag
from django.utils.html import format_html
from django.core.validators import MaxLengthValidator

class SearchForm(forms.Form):
    title = forms.CharField(label='タイトル',max_length=200, required=True)

class MyForm(forms.ModelForm):
    tags = forms.CharField(
        max_length=8,
        validators=[MaxLengthValidator(8)]
        )

    class Meta:
        model = MyModel
        fields = ['title','number','image','tags']

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags.count() > 6:
            raise forms.ValidationError(format_html("タグの数は6つ以下である必要があります。"))
        return tags

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields =['cinema','review','datetime']
