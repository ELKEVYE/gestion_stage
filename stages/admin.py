from django.contrib import admin
from .models import OffreStage

@admin.register(OffreStage)
class OffreStageAdmin(admin.ModelAdmin):
    list_display = ['titre', 'entreprise', 'statut', 'date_limite', 'date_publication']
    list_filter = ['statut', 'entreprise']
    search_fields = ['titre', 'entreprise__nom']
