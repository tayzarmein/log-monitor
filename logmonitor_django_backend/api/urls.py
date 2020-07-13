from django.urls import path

from . import views

urlpatterns = [
    path('gclogs', views.gclogs, name='gclogs')
]