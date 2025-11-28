from django.contrib import admin
from .models import Addproperty, Listproperties, SavedProperty


# Register your models here.
admin.site.register(Addproperty)
admin.site.register(Listproperties)
admin.site.register(SavedProperty)
