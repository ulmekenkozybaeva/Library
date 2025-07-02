from django import forms
from .models import *
from django.utils.text import slugify


class BookForm(forms.ModelForm):
    new_genre = forms.CharField(
        required=False,
        label="Или введите новый жанр",
        help_text="Оставьте пустым, если выбираете существующий жанр"
    )

    class Meta:
        model = DetailedBook
        fields = [
            'name',
            'author',
            'genre',
            'description',
            'image',
            'url',
            'number_of_pages'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'url': forms.URLInput(attrs={'placeholder': 'https://example.com/book'}),
        }
        help_texts = {
            'url': "Url field  to read",
        }

    def clean(self):
        cleaned_data = super().clean()
        genre = cleaned_data.get('genre')
        new_genre = cleaned_data.get('new_genre')

        if not genre and not new_genre:
            raise forms.ValidationError("Выберите жанр или введите новый")

        return cleaned_data

class ExtendedSearchForm(forms.Form):
    book_name = forms.CharField(
        max_length=100,
        label="Название книги",
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Введите название книги", "class": "book_name", 'name': "search_book_name"}
        ),
    )

    author_name = forms.CharField(
        max_length=100,
        label="Автор книги",
        required=False,
        widget=forms.TextInput(
            {"placeholder": "Введите автор книги", "class": "author_name", 'name': "search_author_name"}
        ),
    )
