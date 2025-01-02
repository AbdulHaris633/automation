from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
     path('open-chrome/', views.open_chrome, name='open_chrome')  
]
 