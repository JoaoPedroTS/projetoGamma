from django.contrib import admin
from .models import Batch, Supplier, Protocol

# Register your models here.
admin.site.register(Batch)
admin.site.register(Supplier)
admin.site.register(Protocol)