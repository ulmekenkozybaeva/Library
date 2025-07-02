import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from .models import *


def add_book(request):
  if request.method == 'POST':
    form = BookForm(request.POST, request.FILES)
    if form.is_valid():
      book = form.save(commit=False)

      if form.cleaned_data['new_genre']:
        genre_name = form.cleaned_data['new_genre']
        genre, created = Genre.objects.get_or_create(
          name=genre_name,
          defaults={'slug': slugify(genre_name)}
        )
        book.genre = genre

      if not book.slug:
        base_slug = slugify(book.name)
        book.slug = unique_slugify(book, base_slug)

      book.save()
      return redirect('book_detail', book_slug=form.instance.slug)
  else:
    form = BookForm()

  return render(request, 'add_book.html', {'form': form})


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
