from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin

from rest_framework import permissions, authentication
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Novel, Chapter, Language, Genre, Tag
from .forms import Novel_Form, Chapter_Form
from .serializers import Novel_Serializer

class Novel_CreateView(LoginRequiredMixin, CreateView):
    model = Novel
    form_class = Novel_Form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.uploader = self.request.user
        self.object.save()
        return super().form_valid(form)

class Novel_DetailView(AccessMixin, DetailView):
    model = Novel
    fields = ["name", "author", "artist", "year", "publisher", "licensed", "coo_status", "fully_translated", "genres", "tags", "language"]
    
    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().approved:
            if not request.user.is_authenticated:
                return self.handle_no_permission()
            if not self.request.user.is_staff and self.request.user != self.get_object().uploader:
                return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['chapters'] = Chapter.objects.filter(novel=self.object)
        return context

class Novel_ListView(ListView):
    model = Novel
    
    def get_queryset(self):
        novels = super().get_queryset()
        if 'slug' in self.kwargs:
            try:
                filter_obj = Language.objects.get(slug=self.kwargs['slug'])
                return novels.filter(language=filter_obj, approved=True)
            except Language.DoesNotExist:
                filter_obj = None
            filter_obj = Tag.objects.filter(slug=self.kwargs['slug'])
            if not filter_obj:
                filter_obj = None
            else:
                return novels.filter(tags__in=filter_obj, approved=True)
            filter_obj = Genre.objects.filter(slug=self.kwargs['slug'])
            if not filter_obj:
                raise Http404()
            else:
                return novels.filter(genres__in=filter_obj, approved=True)
        return novels.filter(approved=True)

class Novel_UpdateView(AccessMixin, UpdateView):
    model = Novel
    form_class = Novel_Form
    action = "novel-update"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.request.user.is_staff and self.request.user != self.get_object().uploader:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class Novel_APIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        novel = get_object_or_404(Novel, slug=kwargs['slug'])
        serializer = Novel_Serializer(novel, many=False)
        return Response(serializer.data)

class Novel_DeleteView(AccessMixin, DeleteView):
    model = Novel
    success_url = reverse_lazy("quickscribe:novel-list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.request.user.is_staff and self.request.user != self.get_object().uploader:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class Novel_ApproveView(AccessMixin, View):
    template_name = "quickscribe/novel_approve.html"

    def get(self, request, *args, **kwargs):
        approval_requests = Novel.objects.filter(approved=False)
        return render(request=request, template_name=self.template_name, context={"requests": approval_requests})
    
    def post(self, request, *args, **kwargs):
        filter_obj = request.POST.getlist('request[]')
        approval_requests = Novel.objects.filter(approved=False, id__in=filter_obj)
        if request.POST['submit'] == "Approve":
            approval_requests.update(approved=True)
            return redirect("quickscribe:approve-novel")
        elif request.POST['submit'] == "Decline":
            approval_requests.delete()
            return redirect("quickscribe:approve-novel")
        else:
            raise Http404()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class Chapter_CreateView(LoginRequiredMixin, CreateView):
    model = Chapter
    form_class = Chapter_Form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.novel = Novel.objects.get(slug=self.kwargs['slug'])
        self.object.uploader = self.request.user
        self.object.save()
        return super().form_valid(form)

class Chapter_UpdateView(AccessMixin, UpdateView):
    model = Chapter
    form_class = Chapter_Form
    action = "chapter-update"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.request.user.is_staff and self.request.user != self.get_object().uploader:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class Chapter_DetailView(DetailView):
    model = Chapter
    fields = ["name", 'content', 'novel', 'uploader', 'updated', 'views']

class Chapter_ListView(ListView):
    model = Chapter

class Chapter_DeleteView(AccessMixin, DeleteView):
    model = Chapter

    def get_success_url(self):
        return reverse_lazy("quickscribe:novel-detail", kwargs={'slug': self.object.novel.slug})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.request.user.is_staff and self.request.user != self.get_object().uploader:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
