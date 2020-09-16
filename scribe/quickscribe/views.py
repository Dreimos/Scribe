from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from rest_framework import permissions, authentication
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Novel, Chapter
from .forms import Novel_Form, Chapter_Form
from .serializers import Novel_Serializer

class Novel_CreateView(CreateView):
    model = Novel
    form_class = Novel_Form

class Novel_DetailView(DetailView):
    model = Novel
    fields = ["name", "author", "artist", "year", "publisher", "licensed", "coo_status", "fully_translated", "genres", "tags", "language"]
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['chapters'] = Chapter.objects.filter(novel=self.object)
        return context

class Novel_ListView(ListView):
    model = Novel

class Novel_UpdateView(UpdateView):
    model = Novel
    form_class = Novel_Form
    action = "novel-update"

class Novel_APIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        novel = get_object_or_404(Novel, slug=kwargs['slug'])
        serializer = Novel_Serializer(novel, many=False)
        return Response(serializer.data)

class Chapter_CreateView(CreateView):
    model = Chapter
    form_class = Chapter_Form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.novel = Novel.objects.get(slug=self.kwargs['slug'])
        self.object.uploader = self.request.user
        self.object.save()
        return super().form_valid(form)

class Chapter_UpdateView(UpdateView):
    model = Chapter
    form_class = Chapter_Form
    action = "chapter-update"

class Chapter_DetailView(DetailView):
    model = Chapter
    fields = ["name", 'content', 'novel', 'uploader', 'updated', 'views']

class Chapter_ListView(ListView):
    model = Chapter
