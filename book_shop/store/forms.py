from django import forms
from .models import *


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
