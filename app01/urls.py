from  django.urls import include, path
from django.contrib import admin
from . import views as v1

app_name = 'app01'

urlpatterns = [

    path('listFolhaResumo', v1.listFolhaResumo, name='listFolhaResumo'),
    path('imprimirCSVFolha', v1.imprimirCSVFolha, name='imprimirCSVFolha'),
    path('importacaoFolhaExcel', v1.importacaoFolhaExcel, name='importacaoFolhaExcel'),
    path('planilhaErrada', v1.planilhaErrada, name='planilhaErrada'),
    path('listSomaEventos', v1.listSomaEventos, name='listSomaEventos'),
    path('consultarTabelas', v1.consultarTabelas, name='consultarTabelas'),
    path('folhasProcessadas', v1.folhasProcessadas, name='folhasProcessadas'),
    path('imprimirFolhaLayout', v1.imprimirFolhaLayout, name='imprimirFolhaLayout'),
]

