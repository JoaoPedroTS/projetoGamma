from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Batch
from farm.models import Farm
from season.models import Season
from .forms import BatchForm, EditBatchForm, WorkDayForm, SupplierForm, ProtocolForm, ShapingForm
from .tables import BatchTable

# Create your views here.

#Lista de lotes
@login_required
def batch_index(request, farm_id, season_id):
    season = Season.objects.get(id=season_id)
    farm = Farm.objects.get(id=farm_id)
    batch_list = Batch.objects.filter(farm=farm, season=season).order_by('id')

    #Search
    batch_name = request.GET.get("batch_name")
    if batch_name != "" and batch_name is not None:
        batch_list = batch_list.filter(batch_name__icontains = batch_name)

    #Pagination
    paginator = Paginator(batch_list, 9)
    page = request.GET.get("page")
    batch_list = paginator.get_page(page)
    
    context = {
        "season": season,
        "farm": farm,
        "batch_list": batch_list,
    }

    return render(request, "batch/batch-index.html", context)

#Cadastrar lotes
@login_required
def add_batch(request, season_id, farm_id):
    season = Season.objects.get(id=season_id)
    farm = Farm.objects.get(id=farm_id)
    
    form = BatchForm(request.POST or None)

    if form.is_valid():
        batch = form.save(commit=False)
        batch.farm = farm
        batch.season = season
        batch.save()

        return redirect("batch_index", farm_id=farm_id , season_id=season_id)
    
    context = {
        "form": form
    }
    return render(request, "batch/batch-form.html", context)

#Editar lotes
@login_required
def edit_batch(request, id):
    batch = Batch.objects.get(id=id)
    form = EditBatchForm(request.POST or None, instance=batch)

    if form.is_valid():
        form.save()
        return redirect("batch_detail", batch_id=id)
    
    context = {
        "form": form,
        "batch": batch
    }
    return render(request, "batch/batch-edit-form.html", context)

#Deletar lotes
'''
Opções para apagar o lote 
opção 1: Ao apagar um lote com filho, os filho vão ser apagados também
opção 2: Impedir que um lote com filho seja apagado
opção 3: Ao apagar um lote com filho, os filho vão perde a referencia e vão se tornar 'lotes cabeceira'
'''
@login_required
def delete_batch(request, batch_id, season_id, farm_id):
    batch = Batch.objects.get(id=batch_id)

    if request.method == "POST":
        batch.delete()
        return redirect("batch_index", season_id=season_id, farm_id=farm_id)
    
    context = {
        "batch": batch
    }
    
    return render(request, 'batch/delete-batch.html', context)

#Visão detalhada dos lotes
@login_required
def batch_detail(request, batch_id):
    batch = Batch.objects.get(pk=batch_id)

    context = {
        "batch": batch,
    }

    return render(request, "batch/detail.html", context)

@login_required
def add_workday(request, batch_id):
    batch = Batch.objects.get(pk=batch_id)
    form = WorkDayForm(request.POST or None, instance=batch)

    if form.is_valid():
        action = request.POST.get("action")
        work_day = True if action == "continue" else False
        form.save(work_day=work_day)
        return redirect("batch_index", farm_id=batch.farm.id, season_id=batch.season.id)

    context = {
        "batch":batch,
        "form":form
    }

    return render(request, "batch/workdayA.html", context)

def batch_list(request):
    table = BatchTable(Batch.objects.all())
    context = {
        "table": table,
    }
    
    return render(request, "batch/batch_list.html", context)

@login_required
def registrations(request):
    return render(request, "batch/registrations.html")

@login_required
def add_supplier(request):
    form = SupplierForm(request.POST or None)

    if form.is_valid():
        supplier = form.save()
        supplier.save()
        return redirect("registrations")
    
    context = {
        "form": form
    }

    return render(request, "batch/supplier-form.html", context)

@login_required
def add_protocol(request):
    form = ProtocolForm(request.POST or None)

    if form.is_valid():
        protocol = form.save()
        protocol.save()
        return redirect("registrations")
    
    context = {
        "form": form
    }

    return render(request, "batch/protocol-form.html", context)

@login_required
def add_shaping(request):
    form = ShapingForm(request.POST or None)

    if form.is_valid():
        shaping = form.save()
        shaping.save()
        return redirect("registrations")
    
    context = {
        "form": form
    }

    return render(request, "batch/shaping-form.html", context)