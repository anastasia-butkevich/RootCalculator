from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("from_db/", views.from_db, name="from_db"),
    path("manual/", views.manual, name="manual"),
    path("results/", views.results, name="results"),
]
