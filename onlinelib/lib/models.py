from django.db import models
import uuid
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse


def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)


def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    counter = 1
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1
    return unique_slug

class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        db_table = 'store_genre'
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            unique_slug = base_slug
            counter = 1
            while DetailedBook.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
                counter += 1
                if counter > 5:
                    unique_slug = f"{base_slug}-{uuid.uuid4()}"
                    break
            self.slug = unique_slug
        super().save(*args, **kwargs)


class DetailedBook(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='Books', verbose_name="Genre")
    name = models.CharField(max_length=200, verbose_name="Name")
    author = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, verbose_name="Image")
    url = models.URLField(max_length=500, blank=True, verbose_name="External reading URL",
                         help_text="Optional link to read the book online")
    description = models.TextField(blank=True, verbose_name="Description")
    publication_year = models.DateTimeField(auto_now_add=True, verbose_name="Publication year")
    number_of_pages = models.PositiveIntegerField(null=False, default=0)
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = unique_slugify(self, base_slug)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'store_books'
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

