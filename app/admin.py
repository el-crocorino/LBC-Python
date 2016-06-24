from django.contrib import admin

# Register your models here.
from .models import Rummage, Criteria, Rummage_item, Note

admin.site.register(Rummage)
admin.site.register(Criteria)
admin.site.register(Rummage_item)
admin.site.register(Note)