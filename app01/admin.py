from django.contrib import admin

from django.apps import apps

from .models import ProvDesc

# my custom registration



class ProvDescAdmin(admin.ModelAdmin):
    fields = ['codigo','tipo','descricao','id_municipio']
    search_fields = ['codigo','descricao','tipo','id_municipio']



admin.site.register(ProvDesc, ProvDescAdmin)


