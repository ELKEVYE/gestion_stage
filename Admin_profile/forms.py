from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Etudiant, Filiere, Groupe, RapportStage

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autocomplete': 'off', 'value': '', 'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput())


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']

class EtudiantForm(forms.ModelForm):
  
    class Meta:
        model = Etudiant
        fields = ['matricule','nom', 'prenom', 'email', 'filiere', 'groupe']

class EtudiantImportForm(forms.Form):
    file = forms.FileField(label="Importer un fichier Excel")


class AutoEvaluationForm(forms.Form):
    relation_avec_encadrant = forms.ChoiceField(
        label="Relation avec votre encadrant",
        choices=[(i, i) for i in range(1, 6)],
        widget=forms.RadioSelect
    )
    satisfaction_taches = forms.ChoiceField(
        label="Satisfaction des tâches confiées",
        choices=[(i, i) for i in range(1, 6)],
        widget=forms.RadioSelect
    )
    utilite_du_stage = forms.ChoiceField(
        label="Utilité du stage pour votre formation",
        choices=[(i, i) for i in range(1, 6)],
        widget=forms.RadioSelect
    )
    commentaires = forms.CharField(
        label="Commentaires",
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        required=False
    )

   

class FeedbackEntrepriseForm(forms.Form):
    entreprise = forms.CharField(label="Nom de l'entreprise", max_length=255)
    etudiant = forms.CharField(label="Nom de l'étudiant", max_length=255)
    performance = forms.CharField(label="Performance de l'étudiant", widget=forms.Textarea)
    commentaires = forms.CharField(label="Commentaires", widget=forms.Textarea, required=False)




class RapportStageForm(forms.ModelForm):
    class Meta:
        model = RapportStage
        fields = ['titre', 'fichier']