"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from . import views
from django.urls import path

urlpatterns = [
    path("<int:farm_id>/season/<int:season_id>", views.batch_index, name="batch_index"),
    path("add/<int:farm_id>/season/<int:season_id>", views.add_batch, name="add_batch"),
    path("edit/<int:id>", views.edit_batch, name="edit_batch"),
    path("delete/<int:batch_id>/<int:season_id>/<int:farm_id>", views.delete_batch, name="delete_batch"),
    path("detail/<int:batch_id>/", views.batch_detail, name="batch_detail"),
    path("workday/<int:batch_id>", views.add_workday, name="add_workday"),
    path('table/', views.batch_list, name='batch_list'),
    path("registrations/", views.registrations, name="registrations"),
    path("add_supplier/", views.add_supplier, name="add_supplier"),
    path("add_protocol/", views.add_protocol, name="add_protocol"),
    path("add_shaping/", views.add_shaping, name="add_shaping"),
]