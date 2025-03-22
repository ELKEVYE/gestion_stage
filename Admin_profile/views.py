from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import FeedbackEntrepriseForm, LoginForm, RapportStageForm,  UserUpdateForm
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Etudiant, RapportStage
from .forms import EtudiantForm
import pandas as pd
from .forms import EtudiantImportForm
from django.contrib import messages
from .models import Etudiant, Filiere, Groupe
from .forms import AutoEvaluationForm
from django.contrib import messages
from django.http import HttpResponse



def forgot_password(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "Registration/password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': get_current_site(request).domain, 
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)), 
                        "user": user,
                        'token': default_token_generator.make_token(user), 
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                    except:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    else:
        password_reset_form = PasswordResetForm()
    return render(request=request, template_name="Registration/password_reset_form.html", context={"password_reset_form": password_reset_form})

def homePage(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirection vers la page de connexion si non authentifié
    return render(request, 'homePage.html', {'user': request.user})


def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        

        if user is not None:
            login(request, user)
            return redirect('homePage')  
        else:

            messages.error(request, 'Informations de connexion invalides')
            form = LoginForm(request.POST)  # Afficher les erreurs de validation
    else:
        form = LoginForm()  # Formulaire vide

    return render(request, 'loginPage.html', {'form': form})

# ==============================
# PAGE D'INSCRIPTION
# ==============================
def registerPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, "Compte créé avec succès ! Connectez-vous maintenant.")
            return redirect('loginPage')  # Redirection vers la page de connexion

    return render(request, 'registerPage.html')

# ==============================
# PAGE DE DÉCONNEXION
# ==============================
def logoutPage(request):
    logout(request)
    return redirect('loginPage')  # Redirection vers la page de connexion
from django.shortcuts import render

def password_reset_done(request):
    return render(request, "Registration/password_reset_done.html")
def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect("password_reset_complete")
        else:
            form = SetPasswordForm(user)
        return render(request, "Registration/password_reset_confirm.html", {"form": form})
    else:
        return render(request, "Registration/password_reset_invalid.html")
def password_reset_complete(request):
    return render(request, 'registration/password_reset_complete.html')    


# Liste des étudiants
class EtudiantListView(ListView):
    model = Etudiant
    template_name = 'Etudiant/etudiant_list.html'
    context_object_name = 'etudiants'


# Détails d'un étudiant
class EtudiantDetailView(DetailView):
    model = Etudiant
    template_name = 'Etudiant/etudiant_detail.html'
    context_object_name = 'etudiant'


# Ajouter un étudiant
# class EtudiantCreateView(CreateView):
#     model = Etudiant
#     form_class = EtudiantForm
#     template_name = 'Etudiant/etudiant_form.html'
#     success_url = reverse_lazy('etudiant_list')


# Modifier un étudiant
class EtudiantUpdateView(UpdateView):
    model = Etudiant
    form_class = EtudiantForm
    template_name = 'Etudiant/etudiant_form.html'
    success_url = reverse_lazy('etudiant_list')


# Supprimer un étudiant
class EtudiantDeleteView(DeleteView):
    model = Etudiant
    template_name = 'Etudiant/etudiant_confirm_delete.html'
    success_url = reverse_lazy('etudiant_list')

def import_etudiants(request):
    if request.method == "POST":
        form = EtudiantImportForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES["file"]
            try:
                df = pd.read_excel(excel_file)

                for _, row in df.iterrows():
                    filiere, _ = Filiere.objects.get_or_create(nom=row["filiere"])
                    # groupe, _ = Groupe.objects.get_or_create(nom=row["groupe"])

                    Etudiant.objects.create(
                        matricule=row["matricule"],
                        nom=row["nom"],
                        prenom=row["prenom"],
                        email=row["email"],
                        filiere=filiere,
                        # groupe=groupe
                    )

                messages.success(request, "Importation réussie !")
                return redirect("etudiant_list")

            except Exception as e:
                messages.error(request, f"Erreur lors de l'importation : {e}")

    else:
        form = EtudiantImportForm()

    return render(request, "Etudiant/etudiant_import.html", {"form": form})


def remplir_auto_evaluation(request):
    if request.method == 'POST':
        # Créer une instance du formulaire avec les données envoyées
        form = AutoEvaluationForm(request.POST)
        
        # Vérifier si le formulaire est valide
        if form.is_valid():
            # Récupérer les données envoyées par le formulaire
            nom = request.POST.get('nom')
            prenom = request.POST.get('prenom')
            email = request.POST.get('email')

            evaluation = {
                "nom": nom,
                "prenom": prenom,
                "email": email,
                "relation_avec_encadrant": form.cleaned_data['relation_avec_encadrant'],
                "satisfaction_taches": form.cleaned_data['satisfaction_taches'],
                "utilite_du_stage": form.cleaned_data['utilite_du_stage'],
                "commentaires": form.cleaned_data['commentaires'],
            }

            # Ajouter l'évaluation à la session
            if 'evaluations' not in request.session:
                request.session['evaluations'] = []
            request.session['evaluations'].append(evaluation)
            request.session.modified = True  # Indiquer que la session a été modifiée

            # Afficher un message de succès
            messages.success(request, "Votre auto-évaluation a été soumise avec succès.")
            return redirect('merci')  # Rediriger vers la page de confirmation

    else:
        form = AutoEvaluationForm()  # Si ce n'est pas une soumission, afficher un formulaire vide

    return render(request, 'auto_evaluation/remplir_evaluation.html', {'form': form})
def lire_evaluations(request):
    # Récupérer les évaluations stockées dans la session
    evaluations = request.session.get('evaluations', [])
    return render(request, 'auto_evaluation/liste_evaluations.html', {'evaluations': evaluations})


def merci(request):
    return render(request, 'auto_evaluation/merci.html')

def supprimer_evaluations(request):
    # Supprimer les évaluations de la session
    if 'evaluations' in request.session:
        del request.session['evaluations']
    
    # Redirection vers la page des évaluations
    return redirect('lire_evaluations')


def feedback_entreprise(request):
    if request.method == 'POST':
        # Utiliser le formulaire sans modèle
        form = FeedbackEntrepriseForm(request.POST)
        
        if form.is_valid():
            # Récupérer les données du formulaire
            entreprise = form.cleaned_data['entreprise']
            etudiant = form.cleaned_data['etudiant']
            performance = form.cleaned_data['performance']
            commentaires = form.cleaned_data['commentaires']

            # Traiter les données - ici, on peut les enregistrer en session ou les envoyer par email
            feedback_data = {
                "entreprise": entreprise,
                "etudiant": etudiant,
                "performance": performance,
                "commentaires": commentaires,
            }

            # Exemple : sauvegarder dans la session pour affichage ultérieur
            if 'feedbacks' not in request.session:
                request.session['feedbacks'] = []

            request.session['feedbacks'].append(feedback_data)
            request.session.modified = True

            messages.success(request, "Le feedback a été soumis avec succès.")
            return redirect('merci_feedback')
    else:
        form = FeedbackEntrepriseForm()

    return render(request, 'auto_evaluation/feedback_entreprise.html', {'form': form})

def afficher_feedbacks(request):
    # Récupérer les feedbacks enregistrés dans la session
    feedbacks = request.session.get('feedbacks', [])
    return render(request, 'auto_evaluation/liste_feedbacks.html', {'feedbacks': feedbacks})

def merci_feedback(request):
    return render(request, 'auto_evaluation/merci_feedback.html')

def supprimer_feedback(request, index):
    feedbacks = request.session.get('feedbacks', [])
    
    # Vérifier si l'index est valide
    if 0 <= index < len(feedbacks):
        del feedbacks[index]
        request.session['feedbacks'] = feedbacks
        request.session.modified = True  # Marquer la session comme modifiée
        messages.success(request, "Le feedback a été supprimé avec succès.")
    else:
        messages.error(request, "Feedback non trouvé.")
    
    return redirect('lire_feedbacks')


def homeEtudiant(request):
    if not request.user.is_authenticated:
        return redirect('login')  
    return render(request, 'Entreprise.html', {'user': request.user})
def homeEtudiants(request):
    if not request.user.is_authenticated:
        return redirect('login')  
    return render(request, 'Etudiant.html', {'user': request.user})


def soumettre_rapport(request):
        if request.method == 'POST':
            form = RapportStageForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('mes_rapports')
        else:
            form = RapportStageForm()
        return render(request, 'Rapport/soumettre_rapport.html', {'form': form})


def liste_rapports(request):
        rapports = RapportStage.objects.all()  # Récupère tous les rapports
        return render(request, 'Rapport/liste_rapports.html', {'rapports': rapports}) 
    