from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Farm
from season.models import Season
import json

# Create your views here.

# Listar fazendas
@login_required
def farm_index(request, season_id=None):
    farm_list = None
    season = None

    if season_id is None:
        farm_list = Farm.objects.all()
    else:
        season = Season.objects.get(id=season_id)
        farm_list = season.farms.all()
    
    context = {
        "season": season,
        "farm_list": farm_list,
    }

    return render(request, "farm/farm-index.html", context)

#Visão detalhada da fazenda
def farm_detail(request, farm_id, season_id=None):
    season = None
    farm = None

    if season_id is None:
        farm = Farm.objects.get(id=farm_id)
    else:
        season = Season.objects.get(id=season_id)
        farm = Farm.objects.get(id=farm_id)

    
    labels = ["Label 1", "Label 2", "Label 3"]
    data = [30, 20, 10]
    
    context = {
        "season": season,
        "farm": farm,
        "labels": labels,
        'data': data
    }

    return render(request, "farm/detail.html", context)