from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view),
    path('home/', views.home_view, name='home'),
    path("api/work-orders/", include("work_orders.urls")),
    path("invoice/",include("invoice.urls")),
]
