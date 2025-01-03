from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Sum
from .models import Batch, Supplier, Protocol
from farm.models import Farm
from season.models import Season
from .forms import BatchForm, EditBatchForm, WorkDayForm, SupplierForm, ProtocolForm, UncertaintyForm, RecurrenceForm
from .tables import BatchTable

# Create your views here.

#Lista de lotes
@login_required
def batch_index(request, farm_id, season_id):
    season = Season.objects.get(id=season_id)
    farm = Farm.objects.get(id=farm_id)
    batch_list = Batch.objects.filter(farm=farm, season=season).order_by('id')
    total_animals = Batch.objects.filter(farm=farm, season=season, prior_batch__isnull=True).aggregate(Sum('batch_size'))['batch_size__sum'] or 0

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
        "total_animals": total_animals
    }

    return render(request, "batch/batch-index.html", context)

#Cadastrar lotes
@login_required
def add_batch(request, season_id, farm_id):
    season = Season.objects.get(id=season_id)
    farm = Farm.objects.get(id=farm_id)
    
    form = BatchForm(request.POST or None)

    print("Dados do POST:", request.POST)

    if request.method == "POST":
        print(request.POST)
        if form.is_valid():
            batch = form.save(commit=False)
            batch.farm = farm
            batch.season = season
            batch.save()
            form.save_m2m()

            batch.update_acronym()
            
            return redirect("batch_index", farm_id=farm_id , season_id=season_id)        
    else: 
        print(form.errors)
            
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
        batch = form.save(commit=False)
        batch.save()
        batch.save(update_fields=["batch_acronym"])
        return redirect("batch_detail", batch_id=id)
    else:
        print("Erros no formulário:", form.errors)
    
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
        
        instance = form.save(commit=False)
        instance.work_day = work_day
        instance.save()

        form.save_m2m()  # Salva os dados de ManyToMany se necessários

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
    supplier_list = Supplier.objects.all()
    form = SupplierForm(request.POST or None)
    
    if form.is_valid():
        supplier = form.save()
        supplier.save()
    
    context = {
        "supplier_list": supplier_list,
        "form": form
    }

    return render(request, "batch/supplier-form.html", context)

@login_required
def add_protocol(request):
    protocol_list = Protocol.objects.all()
    form = ProtocolForm(request.POST or None)

    if form.is_valid():
        protocol = form.save()
        protocol.save()        
    
    context = {
        "protocol_list":protocol_list,
        "form": form
    }

    return render(request, "batch/protocol-form.html", context)

@login_required
def dg_uncertainty(request, batch_id):
    batch = Batch.objects.get(id=batch_id)
    form = UncertaintyForm(request.POST or None)

    if form.is_valid():
        positive_add = form.cleaned_data["positive_quant"]
        negative_add = form.cleaned_data["negative_quant"]

        batch.positive_quant += positive_add
        batch.negative_quant += negative_add
        batch.uncertainty_quant -= (positive_add + negative_add)
        batch.save()

        return redirect("batch_detail", batch_id=batch_id)

    context = {
        "batch": batch,
        "form": form
    }
    
    return render(request, "batch/uncertainty-form.html", context)

@login_required
def dg_recurrence(request, batch_id):
    batch = Batch.objects.get(id=batch_id)
    #Como fazer a contabilidade 

    #Falta tratar o caso onde existem um retorno mas n existe lote derivado
    derived_batch = batch.derivative.first()

    form = RecurrenceForm(request.POST or None)

    if form.is_valid():
        recurrence_positive = form.cleaned_data["recurrence_positive_quant"]
        recurrence_negative = form.cleaned_data["recurrence_negative_quant"]

        batch.recurrence_positive_quant += recurrence_positive
        batch.recurrence_quant -= (recurrence_negative + recurrence_positive)
        batch.save()

        if derived_batch:
            derived_batch.batch_size += recurrence_negative
            derived_batch.save()
        
        return redirect("batch_detail", batch_id=batch_id)

    context = {
        "batch": batch,
        "form": form
    }

    return render(request, "batch/recurrence-form.html", context)