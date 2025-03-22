from django.urls import path
from . import views
from .views import (
    EtudiantListView,
    EtudiantDetailView,
    # EtudiantCreateView,
    EtudiantUpdateView,
    EtudiantDeleteView,
    lire_evaluations,
    liste_rapports,
    
    merci,
    remplir_auto_evaluation,
    soumettre_rapport,
)
from .views import EtudiantListView, import_etudiants  # Importer la bonne vue

urlpatterns = [
 path('login/', views.loginPage, name='loginPage'),  # Route pour la page de connexion
    path('register/', views.registerPage, name='registerPage'),  # Route pour l'inscription
    path('logout/', views.logoutPage, name='logoutPage'),  # Route pour la déconnexion
    path('home/', views.homePage, name='homePage'),    
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('password_reset/', views.forgot_password, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password_reset/complete/', views.password_reset_complete, name='password_reset_complete'),

    path('etudiant/', EtudiantListView.as_view(), name='etudiant_list'),
    path('etudiant/<int:pk>/', EtudiantDetailView.as_view(), name='etudiant_detail'),
    # path('etudiant/ajouter/', EtudiantCreateView.as_view(), name='etudiant_ajouter'),
    path('etudiant/<int:pk>/modifier/', EtudiantUpdateView.as_view(), name='etudiant_modifier'),
    path('etudiant/<int:pk>/supprimer/', EtudiantDeleteView.as_view(), name='etudiant_supprimer'),
    path("etudiants/import/", import_etudiants, name="import_etudiants"),

    path('auto-evaluation/', remplir_auto_evaluation, name='remplir_auto_evaluation'),
    path('merci/', merci, name='merci'),
    # path('admin/evaluations/', lire_evaluations, name='lire_evaluations'),
     path('evaluations/', views.lire_evaluations, name='lire_evaluations'),
    path('evaluations/supprimer/', views.supprimer_evaluations, name='supprimer_evaluations'),

    path('feedback_entreprise/', views.feedback_entreprise, name='feedback_entreprise'),
    path('liste_feedbacks/', views.afficher_feedbacks, name='lire_feedbacks'),
    path('merci_feedback/', views.merci_feedback, name='merci_feedback'),
    path('feedbacks/supprimer/<int:index>/', views.supprimer_feedback, name='supprimer_feedback'),

    path('Entreprise/', views.homeEtudiant, name='Etudiant'),    
    path('Etudiantes/', views.homeEtudiants, name='Etudiant'),    

   path('soumettre/', views.soumettre_rapport, name='soumettre_rapport'),
    path('mes-rapports/', views.liste_rapports, name='mes_rapports'),
]

