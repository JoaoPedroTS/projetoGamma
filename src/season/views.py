from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
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

    #Contagem de animais dentro da estação
    total_batch_size = Batch.objects.filter(
        season=season,
        prior_batch__isnull=True,
    ).aggregate(total=Sum("batch_size"))["total"]

    #Contagem de Lotes por tipo na estação
    batches_types = Batch.objects.filter(season_id=season_id).values('batch_shaping__shaping_name').annotate(total=Count('id'))

    #Contagem de lotes por Responsável técnico
    vets = Batch.objects.filter(season_id=season_id).values('vet_name__username').annotate(total=Count('id'))

    #Contagem de lotes agrupado por `batch_maternity`
    batches_maternity_count = Batch.objects.filter(season_id=season_id).values("batch_maternity").annotate(total=Count("id"))

    season_duration = season.get_duration()

    if season.begin_date > timezone.now().date():
        percent_remaining_days = 0
        remaining_days = season.get_duration()
    else:
        percent_remaining_days = round(((season.get_remaining_days()/season_duration)*100), 2)
        remaining_days = season.get_remaining_days()

    context = {
        "season": season,
        "total_batch_size": total_batch_size,
        "batches_types": batches_types,
        "batches_maternity_count": batches_maternity_count,
        "vets":vets,
        "season_duration": season_duration,
        "remaining_days": remaining_days,
        "percent_remaining_days": percent_remaining_days
    }
    
    return render(request, "season/season-detail.html", context)