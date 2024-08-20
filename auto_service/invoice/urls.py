from django.urls import path
from .views import create_pdf

app_name = 'invoice'

urlpatterns = [path('create-pdf-invoice/<str:pk>', create_pdf, name='create-pdf-invoice'),]