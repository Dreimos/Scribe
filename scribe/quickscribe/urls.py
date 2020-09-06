from django.urls import path


from .views import Novel_CreateView, Novel_DetailView
app_name = "quickscribe"

urlpatterns = [
    path("novel/new/", Novel_CreateView.as_view(), name="novel-create"),
    path("novel/<slug:slug>/", Novel_DetailView.as_view(), name="novel-detail"),
]
