import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *


def book_list(request):
    books = DetailedBook.objects.all()
    return render(request, 'bookshops.html', {'books': books})


def extended_search(request):
  extended_search_form = ExtendedSearchForm(request.GET or None)
  found_books = None
  show_results = False

  if request.method == 'GET' and extended_search_form.is_valid():
    search_book = extended_search_form.cleaned_data.get("book_name")
    search_author = extended_search_form.cleaned_data.get("author_name")

    found_books = DetailedBook.objects.all()

    if search_book:
      found_books = found_books.filter(name__icontains=search_book)
    if search_author:
      found_books = found_books.filter(author__icontains=search_author)

    show_results = True

  data = {
    "extended_search_form": extended_search_form,
    "found_books": found_books,
    "show_results": show_results,
  }
  return render(request, "search_results.html", data)


def book_detail(request, book_slug):
  book = get_object_or_404(DetailedBook, slug=book_slug)
  return render(request, 'books.html', {'book': book})
