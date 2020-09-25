from django.urls import path

from .views import (Novel_CreateView,
                    Novel_DetailView,
                    Novel_ListView,
                    Novel_UpdateView,
                    Novel_DeleteView,
                    Novel_APIView,
                    Chapter_CreateView,
                    Chapter_DetailView,
                    Chapter_ListView,
                    Chapter_UpdateView,
                    Chapter_DeleteView)

app_name = "quickscribe"

urlpatterns = [
    path("novel/new/", Novel_CreateView.as_view(), name="novel-create"),
    path("novel/list/", Novel_ListView.as_view(), name="novel-list"),
    path("novel/list/<slug:slug>", Novel_ListView.as_view(), name="novel-list"),
    path("novel/<slug:slug>/", Novel_DetailView.as_view(), name="novel-detail"),
    path("novel/<slug:slug>/update/", Novel_UpdateView.as_view(), name="novel-update"),
    path("novel/<slug:slug>/delete/", Novel_DeleteView.as_view(), name="novel-delete"),
    path("api.novel/<slug:slug>/", Novel_APIView.as_view(), name='api-novel'),
    path("chapter/new/<slug:slug>/", Chapter_CreateView.as_view(), name="chapter-create"),
    path("chapter/<int:pk>/", Chapter_DetailView.as_view(), name="chapter-detail"),
    path("chapter/<int:pk>/update/", Chapter_UpdateView.as_view(), name="chapter-update"),
    path("chapter/list/", Chapter_ListView.as_view(), name="chapter-list"),
    path("chapter/<int:pk>/delete/", Chapter_DeleteView.as_view(), name="chapter-delete"),
]
