from django.urls import path

from .views import (Novel_CreateView,
                    Novel_DetailView,
                    Novel_ListView,
                    Chapter_CreateView,
                    Chapter_DetailView,
                    Chapter_ListView)

app_name = "quickscribe"

urlpatterns = [
    path("novel/new/", Novel_CreateView.as_view(), name="novel-create"),
    path("novel/list/", Novel_ListView.as_view(), name="novel-list"),
    path("novel/<slug:slug>/", Novel_DetailView.as_view(), name="novel-detail"),
    path("upload/<slug:slug>/", Chapter_CreateView.as_view(), name="chapter-create"),
    path("chapter/<int:pk>/", Chapter_DetailView.as_view(), name="chapter-detail"),
    path("chapter/list/", Chapter_ListView.as_view(), name="chapter-list"),
]
