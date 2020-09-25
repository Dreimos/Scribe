from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from rest_framework import permissions, authentication
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Novel, Chapter, Language, Genre, Tag
from .forms import Novel_Form, Chapter_Form
from .serializers import Novel_Serializer

class Novel_CreateView(LoginRequiredMixin, CreateView):
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
    
    def get_queryset(self):
        if 'slug' in self.kwargs:
            novels = super().get_queryset()
            try:
                filter_obj = Language.objects.get(slug=self.kwargs['slug'])
                return novels.filter(language=filter_obj)
            except Language.DoesNotExist:
                filter_obj = None
            filter_obj = Tag.objects.filter(slug=self.kwargs['slug'])
            if not filter_obj:
                filter_obj = None
            else:
                return novels.filter(tags__in=filter_obj)
            filter_obj = Genre.objects.filter(slug=self.kwargs['slug'])
            if not filter_obj:
                raise Http404()
            else:
                return novels.filter(genres__in=filter_obj)
        return super().get_queryset()

class Novel_UpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Novel
    form_class = Novel_Form
    action = "novel-update"

    def test_func(self):
        if self.request.user == self.get_object().uploader:
            return True
        else:
            return self.request.user.is_staff

class Novel_APIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        novel = get_object_or_404(Novel, slug=kwargs['slug'])
        serializer = Novel_Serializer(novel, many=False)
        return Response(serializer.data)

class Novel_DeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Novel
    success_url = reverse_lazy("quickscribe:novel-list")

    def test_func(self):
        if self.request.user == self.get_object().uploader:
            return True
        else:
            return self.request.user.is_staff

class Chapter_CreateView(LoginRequiredMixin, CreateView):
    model = Chapter
    form_class = Chapter_Form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.novel = Novel.objects.get(slug=self.kwargs['slug'])
        self.object.uploader = self.request.user
        self.object.save()
        return super().form_valid(form)

class Chapter_UpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Chapter
    form_class = Chapter_Form
    action = "chapter-update"

    def test_func(self):
        if self.request.user == self.get_object().uploader:
            return True
        else:
            return self.request.user.is_staff

class Chapter_DetailView(DetailView):
    model = Chapter
    fields = ["name", 'content', 'novel', 'uploader', 'updated', 'views']

class Chapter_ListView(ListView):
    model = Chapter

class Chapter_DeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Chapter

    def get_success_url(self):
        return reverse_lazy("quickscribe:novel-detail", kwargs={'slug': self.object.novel.slug})

    def test_func(self):
        if self.request.user == self.get_object().uploader:
            return True
        else:
            return self.request.user.is_staff
