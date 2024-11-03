from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from .models import Farm
from batch.models import Batch
from .forms import FarmForm
from season.models import Season

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
    batches_count = 0
    animals_count = 0
    positive_count = 0
    negative_count = 0

    if season_id is None:
        farm = Farm.objects.get(id=farm_id)
    else:
        season = Season.objects.get(id=season_id)
        farm = Farm.objects.get(id=farm_id)
        batches_count = Batch.objects.filter(farm=farm, season=season).count()
        animals_count = Batch.objects.filter(farm=farm, season=season, prior_batch__isnull=True).aggregate(total=Sum("batch_size"))["total"]
        positive_count = Batch.objects.filter(farm=farm, season=season).aggregate(total=Sum("positive_quant"))["total"]
        negative_count = Batch.objects.filter(farm=farm, season=season).aggregate(total=Sum("negative_quant"))["total"]
    
    context = {
        "season": season,
        "farm": farm,
        "batches_count": batches_count,
        "animals_count": animals_count,
        "positive_count": positive_count,
        "negative_count": negative_count
    }

    return render(request, "farm/detail.html", context)

@user_passes_test(lambda u: u.is_superuser)
def add_farm(request):
    form = FarmForm(request.POST or None)

    if form.is_valid():
        farm = form.save()
        farm.save()
        return redirect("farm_index")

    context = {
        "form": form
    }
    
    return render(request, "farm/add-farm.html", context)