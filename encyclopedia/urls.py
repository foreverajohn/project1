from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/new", views.new, name="new"),
    path("wiki/edit", views.edit, name="edit"),
    path("wiki/search", views.search, name="search"),
    path("wiki/random", views.random, name="random"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("wiki/<str:entry>/edit", views.edit, name="edit")
]
