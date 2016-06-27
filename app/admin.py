from django.contrib import admin

# Register models here.
from .models import Rummage, Criteria, Rummage_item, Note

class RummageAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_date', 'updated_date')
    list_filter = ('user',)   
    date_hierarchy = 'created_date'
    ordering = ('created_date',)
    search_fields = ('title', 'url')
    
class Rummage_itemAdmin(admin.ModelAdmin):
    list_display = ('rummage', 'name', 'created_date', 'updated_date')
    list_filter = ('rummage',)   
    date_hierarchy = 'created_date'
    ordering = ('created_date',)
    search_fields = ('title', 'url')

class CriteriaAdmin(admin.ModelAdmin):
    list_display = ('rummage', 'name', 'weight', 'created_date', 'updated_date')
    list_filter = ('rummage', 'weight')   
    date_hierarchy = 'created_date'
    ordering = ('created_date',)
    search_fields = ('title', 'weight', 'url')    
    
class NoteAdmin(admin.ModelAdmin):
    list_display = ('rummage_item', 'criteria', 'note', 'created_date', 'updated_date')
    list_filter = ('rummage_item', 'criteria')   
    date_hierarchy = 'created_date'
    ordering = ('created_date',)
    search_fields = ('criteria', 'note')    
    

admin.site.register(Rummage, RummageAdmin)
admin.site.register(Criteria, CriteriaAdmin)
admin.site.register(Rummage_item, Rummage_itemAdmin)
admin.site.register(Note, NoteAdmin)
