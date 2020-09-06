from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView

from .models import Novel, Chapter
from .forms import Novel_Form

class Novel_CreateView(CreateView):
    model = Novel
    form_class = Novel_Form

class Novel_DetailView(DetailView):
    model = Novel
    fields = ["name", "author", "artist", "year", "publisher", "licensed", "coo_status", "fully_translated", "genres", "tags", "language"]
