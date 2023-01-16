"""jose_cuervo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from cuervo.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),

    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register_token, name="register"),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('inventoryLocation/', inventoryLocation_view, name='inventoryLocation'),
    path('labelStatus/', labelStatus_view, name='labelStatus'),
    path('coilHandling/', coilHandling_view, name='coilHandling'),
    path('depletionOfCoils/', depletionOfCoils_view, name='depletionOfCoils'),
    path('marbeteHandling/', labelHandling_view, name='labelHandling'),
    path('usersManagement/', usersManagement_view, name='usersManagement'),
    path('labelTraceability/', labelTraceability_view, name='labelTraceability'),
    path('reports/', reports_view, name='reports'),
]

urlpatterns += staticfiles_urlpatterns()
