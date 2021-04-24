"""TEProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from projdir.views import homepage, mainpage, dashboard
from projdir.views import co2_add_dataset, co2_view, co2_predict, co2_loading, co2_truncate, co2_table
from projdir.views import temp_add_dataset, temp_view, temp_predict, temp_loading, temp_truncate, temp_table
from projdir.views import glacier_add_dataset, glacier_view, glacier_predict, glacier_loading, glacier_truncate, glacier_table

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage),
    path('dashboard/', dashboard),
    path('mainpage/', mainpage),
    path('co2_add_dataset/', co2_add_dataset),
    path('co2_view/', co2_view),
    path('co2_predict/', co2_predict),
    path('co2_import/', co2_loading),
    path('co2_truncate', co2_truncate),
    path('co2_table/', co2_table),
    path('temp_add_dataset/', temp_add_dataset),
    path('temp_view/', temp_view),
    path('temp_predict/', temp_predict),
    path('temp_import/', temp_loading),
    path('temp_truncate', temp_truncate),
    path('temp_table/', temp_table),
    path('glacier_add_dataset/', glacier_add_dataset),
    path('glacier_view/', glacier_view),
    path('glacier_predict/', glacier_predict),
    path('glacier_import/', glacier_loading),
    path('glacier_truncate', glacier_truncate),
    path('glacier_table/', glacier_table),
]
