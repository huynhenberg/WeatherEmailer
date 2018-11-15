from django.urls import path

from . import views

app_name = 'subscription'

urlpatterns = [
    path('', views.index, name='index'),
    path('nosubmit/', views.nosubmit, name='nosubmit'),
    path('submit/', views.submit, name='submit'),
    path('submitted/', views.submitted, name='submitted'),
]
