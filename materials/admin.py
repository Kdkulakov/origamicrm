from django.contrib import admin
from .models import Material, MaterialCategory, MaterialUnits, MaterialInstance


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'short_desc', 'count', 'count_full', 'updated', 'created'
    ]
    # readonly_fields = ['count']

    list_filter = [
        'name',
        'category',
        'created',
        'updated'
    ]

    search_fields = [
        'name',
        'category',
        'short_desc'
    ]

admin.site.register(MaterialCategory)
admin.site.register(MaterialUnits)


@admin.register(MaterialInstance)
class MaterialInstanceAdmin(admin.ModelAdmin):
    list_display = [
        'material', 'updated', 'created'
    ]
    list_filter = [
        'material',
        'created',
        'updated'
    ]