from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("files/", views.file_list, name="files"),
    path("upload/", views.upload_file, name="upload"),
    path("download/<int:pk>/", views.download_file, name="download"),
    path("delete/<int:pk>/", views.delete_file, name="delete"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
]