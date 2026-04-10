from django.contrib import admin

from .models import Author, Podcast, Publisher


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'url')
    list_filter = ('author', 'publisher')
    search_fields = ('title', 'url', 'author__name', 'publisher__name')
