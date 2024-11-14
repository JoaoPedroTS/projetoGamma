from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count
from.models import Season
from .forms import SeasonForm, AppendFarmForm
from batch.models import Batch
from farm.models import Farm

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

    # Contagem de retornos
    derivative_batch_size = Batch.objects.filter(
        season=season).exclude(prior_batch=None).aggregate(total=Sum("batch_size")
    )["total"]


    #Contagem de Lotes por tipo na estação
    batches_types = Batch.objects.filter(
        season_id=season_id).values('batch_shapping').annotate(total=Count('id')
    )

    #contagem de lotes por protocolo na estação
    protocols = Batch.objects.filter(
        season_id=season_id).values("protocol__protocol_acronym").annotate(total=Count("id")
    )

    #Contagem de lotes por Responsável técnico
    vets = Batch.objects.filter(
        season_id=season_id).values('vet_name__username').annotate(total=Count('id')
    )

    #Contagem de lotes agrupado por `batch_maternity`
    batches_maternity_count = Batch.objects.filter(
        season_id=season_id).values("batch_maternity").annotate(total=Count("id")
    )

    season_duration = season.get_duration()
    elapsed_days = timezone.now().date() - season.begin_date

    if season.begin_date > timezone.now().date():
        percent_remaining_days = 0
        remaining_days = season.get_duration()
    else:
        percent_remaining_days = round(((elapsed_days.days/season_duration)*100), 2)
        remaining_days = season.get_remaining_days()

    context = {
        "season": season,
        "total_batch_size": total_batch_size,
        "batches_types": batches_types,
        "protocols": protocols,
        "batches_maternity_count": batches_maternity_count,
        "vets":vets,
        "season_duration": season_duration,
        "remaining_days": remaining_days,
        "percent_remaining_days": percent_remaining_days,
        "derivative_batch_size": derivative_batch_size
    }
    
    return render(request, "season/season-detail.html", context)

@user_passes_test(lambda u: u.is_superuser)
def add_season(request):
    # season = Season.objects.get(id=season_id)
    farms = Farm.objects.all()

    form = SeasonForm(request.POST or None)

    if request.method == "POST":
        print(request.POST)  # Para depuração
        if form.is_valid():
            print("Dados limpos para farms:", form.cleaned_data.get("farms"))
            season = form.save(commit=False)
            season.save()
            form.save_m2m()  # Salva a relação ManyToManyField
            return redirect("season_index")
        else:
            print(form.errors)
    
    context = {
        "form": form,
        "farm": farms,
    }

    return render(request, "season/add-season.html", context)

@user_passes_test(lambda u: u.is_superuser)
def append_farm(request, season_id):
    season = Season.objects.get(id=season_id)
    
    form = AppendFarmForm(request.POST or None, instance=season)

    if form.is_valid():
        form.save()
        return redirect("season_detail", season_id = season_id)
    
    context = {
        "form": form,
        "season": season,
    }

    return render(request, "season/append_farm.html", context)