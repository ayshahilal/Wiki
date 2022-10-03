from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>",views.entry_page, name="title"),
    path("search/",views.search, name="search"),
    path("new_page/",views.new_page, name="new_page"),
    path("edit/", views.edit, name="edit"),
    path("save_edit/", views.save_edit, name="save_edit"),
    path("rand/", views.random_page, name="random_page")
]
