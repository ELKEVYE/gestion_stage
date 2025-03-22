from datetime import date
from django import forms
from .models import Entreprise,Encadrant
from .models import Stage
from .models import Soutenance
from .models import OffreStage
from django.utils.timezone import now

class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = ['nom', 'description', 'adresse', 'email']

class EncadrantForm(forms.ModelForm):
    class Meta:
        model = Encadrant
        fields = ['nom', 'prenom', 'etablissement']


class StageForm(forms.ModelForm):
    encadrants = forms.ModelMultipleChoiceField(
        queryset=Encadrant.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=False  # Rend le champ non obligatoire
    )

    class Meta:
        model = Stage
        fields = '__all__'
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
            
        }
class SoutenanceForm(forms.ModelForm):
    class Meta:
        model = Soutenance
        fields = ['stage', 'date_soutenance', 'note', 'commentaire']
        widgets = {
            'date_soutenance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'note': forms.NumberInput(attrs={'class': 'form-control'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_date_soutenance(self):
        # Récupérer la date de soutenance à partir des données nettoyées
        date_soutenance = self.cleaned_data.get('date_soutenance')

        # Vérifie si la date est inférieure à la date actuelle
        if date_soutenance and date_soutenance < date.today():
            raise forms.ValidationError("La date de soutenance ne peut pas être inférieure à la date actuelle.")
        
        return date_soutenance
class OffreStageForm(forms.ModelForm):
    class Meta:
        model = OffreStage
        fields = ['entreprise', 'titre', 'description', 'date_limite']

    def clean_date_limite(self):
        """ Vérifie que la date limite n'est pas antérieure à la date actuelle """
        date_limite = self.cleaned_data.get('date_limite')
        if date_limite < now().date():
            raise forms.ValidationError("La date limite doit être postérieure à aujourd'hui.")
        return date_limite
    

