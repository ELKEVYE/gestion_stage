
from django.shortcuts import render, get_object_or_404, redirect
import csv
from reportlab.lib.pagesizes import letter
from Admin_profile.models import Annee, Etudiant
from .models import Entreprise,Encadrant, Stage,Soutenance
from .forms import EntrepriseForm, StageForm
from .forms import EncadrantForm
from django.utils.timezone import now
from .forms import SoutenanceForm
from django.db.models import Count, Q
from django.utils import timezone
from .models import OffreStage
from .forms import OffreStageForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.contrib import messages
from .utils import generer_pdf_convention, generer_pdf_attestation, generer_pdf_convocation
from reportlab.platypus import Table, TableStyle,SimpleDocTemplate
from reportlab.lib import colors
def entreprise_create(request):
    if request.method == "POST":
        form = EntrepriseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('entreprise_list') 
    else:
        form = EntrepriseForm()
    return render(request, 'stages/entreprise_form.html', {'form': form})


def entreprise_list(request):
    entreprises = Entreprise.objects.all()
    return render(request, 'stages/entreprise_list.html', {'entreprises': entreprises})


def entreprise_detail(request, id):
    entreprise = get_object_or_404(Entreprise, id=id)
    return render(request, 'stages/entreprise_detail.html', {'entreprise': entreprise})


def entreprise_update(request, id):
    entreprise = get_object_or_404(Entreprise, id=id)
    if request.method == "POST":
        form = EntrepriseForm(request.POST, instance=entreprise)
        if form.is_valid():
            form.save()
            return redirect('entreprise_list')
    else:
        form = EntrepriseForm(instance=entreprise)
    return render(request, 'stages/entreprise_form.html', {'form': form})


def entreprise_delete(request, id):
    entreprise = get_object_or_404(Entreprise, id=id)
    if request.method == "POST":
        entreprise.delete()
        return redirect('entreprise_list')
    return render(request, 'stages/entreprise_confirm_delete.html', {'entreprise': entreprise})


def encadrant_list(request):
    encadrants = Encadrant.objects.all()
    
    return render(request, 'encadrant/encadrant_list.html', {'encadrants': encadrants})


def encadrant_detail(request, pk):
    encadrant = get_object_or_404(Encadrant, pk=pk)
    return render(request, 'encadrant/encadrant_detail.html', {'encadrant': encadrant})


def encadrant_create(request):
    if request.method == "POST":
        form = EncadrantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('encadrant_list')
    else:
        form = EncadrantForm()
    return render(request, 'encadrant/encadrant_form.html', {'form': form})


def encadrant_update(request, pk):
    encadrant = get_object_or_404(Encadrant, pk=pk)
    if request.method == "POST":
        form = EncadrantForm(request.POST, instance=encadrant)
        if form.is_valid():
            form.save()
            return redirect('encadrant_list')
    else:
        form = EncadrantForm(instance=encadrant)
    return render(request, 'encadrant/encadrant_form.html', {'form': form})


def encadrant_delete(request, pk):
    encadrant = get_object_or_404(Encadrant, pk=pk)
    if request.method == "POST":
        encadrant.delete()
        return redirect('encadrant_list')
    return render(request, 'encadrant/encadrant_confirm_delete.html', {'encadrant': encadrant})

# Liste des stages
def stage_list(request):
    stages = Stage.objects.all()
    return render(request, 'entreprise/stage_list.html', {'stages': stages})

# Détails d'un stage
def stage_detail(request, pk):
    stage = get_object_or_404(Stage, pk=pk)
    return render(request, 'entreprise/stage_detail.html', {'stage': stage})

# Création d'un stage
def stage_create(request):
    if request.method == "POST":
        form = StageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("stage_list")
        else:
            print(form.errors)  # Débogage pour voir les erreurs
    else:
        form = StageForm()
    return render(request, "entreprise/stage_form.html", {"form": form})

# Mise à jour d'un stage
def stage_update(request, pk):
    stage = get_object_or_404(Stage, pk=pk)
    if request.method == "POST":
        form = StageForm(request.POST, instance=stage)
        if form.is_valid():
            form.save()
            return redirect('stage_list')
    else:
        form = StageForm(instance=stage)
    return render(request, 'entreprise/stage_form.html', {'form': form})

# Suppression d'un stage
def stage_delete(request, pk):
    stage = get_object_or_404(Stage, pk=pk)
    if request.method == "POST":
        stage.delete()
        return redirect('stage_list')
    return render(request, 'entreprise/stage_confirm_delete.html', {'stage': stage})

def statistiques_stages(request):
    today = now().date()

    stats = {
        "Non commencé": Stage.objects.filter(date_debut__gt=today).count(),
        "En cours": Stage.objects.filter(date_debut__lte=today, date_fin__gte=today).count(),
        "Terminé": Stage.objects.filter(date_fin__lt=today).count(),
    }

    return render(request, "statistiques.html", {"stats": stats})
# 🔹 Lire (Liste des soutenances)
def soutenance_list(request):
    soutenances = Soutenance.objects.all()
    return render(request, 'soutenance/soutenance_list.html', {'soutenances': soutenances})

# 🔹 Créer une soutenance
def soutenance_create(request):
    if request.method == "POST":
        form = SoutenanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('soutenance_list')
    else:
        form = SoutenanceForm()
    return render(request, 'soutenance/soutenance_form.html', {'form': form})

# 🔹 Modifier une soutenance
def soutenance_update(request, pk):
    soutenance = get_object_or_404(Soutenance, pk=pk)
    if request.method == "POST":
        form = SoutenanceForm(request.POST, instance=soutenance)
        if form.is_valid():
            form.save()
            return redirect('soutenance_list')
    else:
        form = SoutenanceForm(instance=soutenance)
    return render(request, 'soutenance/soutenance_form.html', {'form': form})

# 🔹 Supprimer une soutenance
def soutenance_delete(request, pk):
    soutenance = get_object_or_404(Soutenance, pk=pk)
    if request.method == "POST":
        soutenance.delete()
        return redirect('soutenance_list')
    return render(request, 'soutenance/soutenance_confirm_delete.html', {'soutenance': soutenance})
    
def statistiques_stages(request):
    # Date actuelle
    today = timezone.now().date()

    stages_valides = Stage.objects.filter(
        soutenance__isnull=False, 
        soutenance__note__isnull=False
    ).count()

    # Stages avec soutenance prévue (peuvent être encore en cours)
    stages_soutenance = Stage.objects.filter(
        soutenance__isnull=False, 
        soutenance__note__isnull=True  # Soutenance prévue mais pas encore notée
    ).count()

    # Stages en cours : 
    # - La date actuelle est entre date_debut et date_fin 
    # - OU le stage a une soutenance prévue
    # - MAIS il ne doit pas être validé
    stages_en_cours = Stage.objects.filter(
    Q(date_debut__lte=today, date_fin__gte=today)  # Stage en cours (débuté mais non terminé)
).exclude(  # Exclure les stages déjà validés
    soutenance__isnull=False, 
    soutenance__note__isnull=False
).count()

    # Calcul des statistiques détaillées
    # Nombre de stages par année
    stages_par_annee = Stage.objects.values('annee__annee').annotate(total=Count('id'))

    # Nombre de stages par filière
    stages_par_filiere = Stage.objects.values('etudiant__filiere__nom').annotate(total=Count('id'))

    # Nombre de stages par entreprise
    stages_par_entreprise = Stage.objects.values('entreprise__nom').annotate(total=Count('id'))

    # Contexte pour le template
    context = {
        'stages_en_cours': stages_en_cours,
        'stages_valides': stages_valides,
        'stages_soutenance': stages_soutenance,
        'stages_par_annee': stages_par_annee,
        'stages_par_filiere': stages_par_filiere,
        'stages_par_entreprise': stages_par_entreprise,
    }

    return render(request, 'statistiques.html', context)


def stage_list(request):
    today = timezone.now().date()

    # Récupérer les critères de recherche
    search_etudiant = request.GET.get('search_etudiant', '')
    search_entreprise = request.GET.get('search_entreprise', '')
    search_encadrant = request.GET.get('search_encadrant', '')
    search_annee = request.GET.get('search_annee', '')
    filter_status = request.GET.get('filter_status', '')

    # Filtrer les stages
    stages = Stage.objects.all()

    # Filtrer par étudiant (nom ou prénom)
    if search_etudiant:
        stages = stages.filter(
            Q(etudiant__nom__icontains=search_etudiant) |
            Q(etudiant__prenom__icontains=search_etudiant)
        )

    # Filtrer par entreprise
    if search_entreprise:
        stages = stages.filter(entreprise__nom__icontains=search_entreprise)

    # Filtrer par encadrant
    if search_encadrant:
        stages = stages.filter(encadrants__nom__icontains=search_encadrant)

# Filtrer par année
    if search_annee:
      stages = stages.filter(annee__annee__icontains=search_annee)


    # Appliquer le filtre de statut
    if filter_status == 'en_cours':
        stages = stages.filter(date_debut__lte=today, date_fin__gte=today, soutenance__isnull=True)
    elif filter_status == 'soutenance':
        stages = stages.filter(soutenance__isnull=False, soutenance__note__isnull=True)
    elif filter_status == 'valide':
        stages = stages.filter(soutenance__isnull=False, soutenance__note__isnull=False)
    elif filter_status == 'attente':
        stages = stages.filter(soutenance__isnull=True) | stages.filter(soutenance__isnull=False, soutenance__note__isnull=True)


    context = {
        'stages': stages,
        'search_etudiant': search_etudiant,
        'search_entreprise': search_entreprise,
        'search_encadrant': search_encadrant,
        'search_annee': search_annee,
        'filter_status': filter_status,
        'today': today,
    }
    return render(request, 'entreprise/stage_list.html', context)


@login_required
def ajouter_offre_stage(request):
    if request.method == 'POST':
        form = OffreStageForm(request.POST)
        if form.is_valid():
            offre = form.save(commit=False)
            offre.save()
            return redirect('offres_stages')
    else:
        form = OffreStageForm()

    return render(request, 'poste/ajouter_offre_stage.html', {'form': form})

def offres_stages(request):
    offres_attente = OffreStage.objects.filter(statut='en_attente')
    offres_validees = OffreStage.objects.filter(statut='validee', date_limite__gte=now().date())
    offres_expirees = OffreStage.objects.filter(date_limite__lt=now().date())
    
    # Supprimer les offres expirées dans les offres validées
    OffreStage.objects.filter(statut='validee', date_limite__lt=now().date()).delete()

    return render(request, 'poste/offres_stages.html', {
        'offres_attente': offres_attente,
        'offres_validees': offres_validees,
        'offres_expirees': offres_expirees
    })

def valider_offre_stage(request, pk):
    offre = get_object_or_404(OffreStage, pk=pk)

    if request.method == 'POST':
        offre.statut = 'validee'
        offre.save()
        messages.success(request, "L'offre de stage a été validée avec succès.")
        return redirect('offres_stages')

    return render(request, 'poste/valider_offre_stage.html', {'offre': offre})

def rejeter_offre_stage(request, pk):
    offre = get_object_or_404(OffreStage, pk=pk)
    
    if request.method == 'POST':
        offre.delete()
        return redirect('offres_stages')

    return render(request, 'poste/rejeter_offre_stage.html', {'offre': offre})

def export_stages_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stages.csv"'

    writer = csv.writer(response)
    
    # En-tête du CSV
    writer.writerow(['Année', 'Filière', 'Entreprise', 'Nombre de Stages'])

    # Récupération des statistiques avec regroupement
    stages_data = Stage.objects.values(
        'annee__annee', 'etudiant__filiere__nom', 'entreprise__nom'
    ).annotate(total=Count('id'))

    # Écriture des données
    for stage in stages_data:
        writer.writerow([
            stage["annee__annee"],
            stage["etudiant__filiere__nom"],
            stage["entreprise__nom"],
            stage["total"]
        ])

    return response
def export_stages_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="stages.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []  # Liste des éléments pour le PDF

    # Récupération des statistiques avec regroupement
    stages_data = Stage.objects.values(
        'annee__annee', 'etudiant__filiere__nom', 'entreprise__nom'
    ).annotate(total=Count('id'))

    # Création du tableau
    table_data = [["Année", "Filière", "Entreprise", "Nombre de Stages"]]  # En-tête
    for stage in stages_data:
        table_data.append([
            stage["annee__annee"],
            stage["etudiant__filiere__nom"],
            stage["entreprise__nom"],
            stage["total"]
        ])

    table = Table(table_data, colWidths=[100, 150, 150, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    # Génération du PDF
    doc.build(elements)

    return response


def generer_convention(request):
    if request.method == 'POST':
        # Récupérer les objets des étudiants, entreprises et encadrants sélectionnés
        etudiant = Etudiant.objects.get(id=request.POST['etudiant'])
        entreprise = Entreprise.objects.get(id=request.POST['entreprise'])
        encadrant = Encadrant.objects.get(id=request.POST['encadrant'])
        
        # Récupérer les dates du formulaire
        date_debut = request.POST['date_debut']
        date_fin = request.POST['date_fin']

        # Générer le PDF pour la convention
        pdf = generer_pdf_convention(etudiant, entreprise, encadrant, date_debut, date_fin)
        
        # Retourner la réponse avec le PDF
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="convention_stage.pdf"'
        return response

    # Récupérer les objets pour le formulaire
    etudiants = Etudiant.objects.all()
    entreprises = Entreprise.objects.all()
    encadrants = Encadrant.objects.all()

    # Afficher le formulaire avec les options disponibles
    return render(request, 'poste/generer_convention.html', {
        'etudiants': etudiants,
        'entreprises': entreprises,
        'encadrants': encadrants,
    })

# Vue pour générer l'attestation de stage
def generer_attestation(request):
    if request.method == 'POST':
        etudiant = Etudiant.objects.get(id=request.POST['etudiant'])
        entreprise = Entreprise.objects.get(id=request.POST['entreprise'])
        statut = request.POST['statut']
        
        # Appel à la fonction pour générer le PDF de l'attestation de stage
        pdf = generer_pdf_attestation(etudiant, entreprise, statut)
        
        # Retourner la réponse PDF
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="attestation_stage.pdf"'
        return response

    # Récupérer les objets pour le formulaire
    etudiants = Etudiant.objects.all()
    entreprises = Entreprise.objects.all()

    # Affichage du formulaire avec les options disponibles
    return render(request, 'poste/generer_attestation.html', {
        'etudiants': etudiants,
        'entreprises': entreprises,
    })

# Vue pour générer la convocation à la soutenance
def generer_convocation(request):
    if request.method == 'POST':
        etudiant = Etudiant.objects.get(id=request.POST['etudiant'])
        date_soutenance = request.POST['date_soutenance']
        lieu_soutenance = request.POST['lieu_soutenance']
        
        # Appel à la fonction pour générer le PDF de la convocation
        pdf = generer_pdf_convocation(etudiant, date_soutenance, lieu_soutenance)
        
        # Retourner la réponse PDF
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="convocation_soutenance.pdf"'
        return response

    # Récupérer les étudiants pour le formulaire
    etudiants = Etudiant.objects.all()

    # Affichage du formulaire avec les options disponibles
    return render(request, 'poste/generer_convocation.html', {
        'etudiants': etudiants,
    })