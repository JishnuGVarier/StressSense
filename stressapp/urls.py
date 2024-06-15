"""
URL configuration for humanstress project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.indexView, name='home'),
    path('predict/', views.predictionView, name='predict'),
    path('login/', views.loginView, name='login'),
    path('register/', views.registerView, name='register'),
    path('about/', views.aboutView, name='about'),
    path('services/', views.servicesView, name='services'),
    path('why/', views.whyView, name='why'),
    path('team/', views.teamView, name='team'),
    path('logout/', views.logout_view, name='logout'),
]
