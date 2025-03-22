from django.urls import path
from . import views
from .views import statistiques_stages

urlpatterns = [
    path('entreprises/', views.entreprise_list, name='entreprise_list'),
    path('entreprises/<int:id>/', views.entreprise_detail, name='entreprise_detail'),
    path('entreprises/ajouter/', views.entreprise_create, name='entreprise_create'),
    path('entreprises/<int:id>/modifier/', views.entreprise_update, name='entreprise_update'),
    path('entreprises/<int:id>/supprimer/', views.entreprise_delete, name='entreprise_delete'),

    path('encadrants/', views.encadrant_list, name='encadrant_list'),
    path('encadrants/<int:pk>/', views.encadrant_detail, name='encadrant_detail'),
    path('encadrants/ajouter/', views.encadrant_create, name='encadrant_create'),
    path('encadrants/modifier/<int:pk>/', views.encadrant_update, name='encadrant_update'),
    path('encadrants/supprimer/<int:pk>/', views.encadrant_delete, name='encadrant_delete'),

     path('stages/', views.stage_list, name='stage_list'),
    path('stages/<int:pk>/', views.stage_detail, name='stage_detail'),
    path('stages/create/', views.stage_create, name='stage_create'),
    path('stages/<int:pk>/update/', views.stage_update, name='stage_update'),
    path('stages/<int:pk>/delete/', views.stage_delete, name='stage_delete'),

    path('statistiques/', statistiques_stages, name='statistiques'),

    path('soutenances/', views.soutenance_list, name='soutenance_list'),
    path('soutenances/ajouter/', views.soutenance_create, name='soutenance_create'),
    path('soutenances/modifier/<int:pk>/', views.soutenance_update, name='soutenance_update'),
    path('soutenances/supprimer/<int:pk>/', views.soutenance_delete, name='soutenance_delete'),

    path('ajouter/', views.ajouter_offre_stage, name='ajouter_offre_stage'),
    path('offres/', views.offres_stages, name='offres_stages'),
    path('valider/<int:pk>/', views.valider_offre_stage, name='valider_offre_stage'),
    path('rejeter/<int:pk>/', views.rejeter_offre_stage, name='rejeter_offre_stage'),

    path('export/csv/', views.export_stages_csv, name='export_stages_csv'),
    path('export/pdf/', views.export_stages_pdf, name='export_stages_pdf'),

    path('generer_convention/', views.generer_convention, name='generer_convention'),
    path('generer_attestation/', views.generer_attestation, name='generer_attestation'),
    path('generer_convocation/', views.generer_convocation, name='generer_convocation'),
    ]
