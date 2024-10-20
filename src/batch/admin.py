from django.contrib import admin
from .models import Batch, Shaping, Supplier, Protocol

# Register your models here.
admin.site.register(Batch)
admin.site.register(Shaping)
admin.site.register(Supplier)
admin.site.register(Protocol)