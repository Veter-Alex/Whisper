from django.urls import path

from .views import DirectoryView

urlpatterns = [
    path("api/directories/", DirectoryView.as_view(), name="directory-list"),
]
