from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("resume/", views.resume_page, name="resume"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
]
