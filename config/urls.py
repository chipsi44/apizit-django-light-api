from django.urls import path

from app import views

urlpatterns = [
    path("health", views.health),
    path("info", views.info),
    path("echo", views.echo),
    path("items/<int:item_id>", views.item),
    path("slow", views.slow),
]
