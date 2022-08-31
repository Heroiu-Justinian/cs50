from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/search', views.search_results, name='search'),
    path('wiki/new', views.newpage, name='newpage'),
    path('wiki/edit/<str:title>',views.edit, name='edit'),
    path('wiki/<str:title>',views.display_title, name='display_entry'),
]
