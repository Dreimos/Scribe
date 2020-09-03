from django.contrib import admin

from .models import Novel, Chapter, Genre, Tag, Language

admin.site.register(Novel)
admin.site.register(Chapter)
admin.site.register(Genre)
admin.site.register(Tag)
admin.site.register(Language)
