from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from.models import Season
from batch.models import Batch

# Create your views here.

#Listar estações
@login_required
def season_index(request):
    season_list = Season.objects.all()
    context = {
        "season_list": season_list,
    }
    
    return render(request, "season/season-index.html", context)

#Visão detalhada da estação
@login_required
def season_detail(request, season_id):
    season = Season.objects.get(pk=season_id)

    total_batch_size = Batch.objects.filter(
        season=season,
        prior_batch__isnull=True,
    ).aggregate(total=Sum("batch_size"))["total"]

    context = {
        "season": season,
        "total_batch_size": total_batch_size,
    }
    
    return render(request, "season/season-detail.html", context)