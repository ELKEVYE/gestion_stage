from django.db import models

from Admin_profile.models import Annee, Etudiant
from django.utils import timezone

# Create your models here.
class Entreprise(models.Model):
    nom = models.CharField(max_length=200)
    description = models.CharField(max_length=100)
    adresse = models.TextField()
    email = models.EmailField()

    class Meta:
        db_table = "entreprise"

class Encadrant(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    etablissement= models.CharField(max_length=100)
    class Meta:
        db_table = "encadrant" 

class Stage(models.Model):
    
    titre = models.CharField(max_length=200)
    description = models.TextField()
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    encadrants = models.ManyToManyField(Encadrant, related_name='stages')
    date_debut = models.DateField()
    date_fin = models.DateField()
    annee = models.ForeignKey(Annee, on_delete=models.CASCADE)

    class Meta:
        db_table = "stage" 

class Soutenance(models.Model):
    stage = models.OneToOneField(Stage, on_delete=models.CASCADE)
    date_soutenance = models.DateField()
    note = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)  # Ajout de null=True
    commentaire = models.TextField(blank=True)
class Meta:
        db_table = "soutenance" 


class OffreStage(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    description = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=20,
        choices=[('en_attente', 'En Attente'), ('validee', 'Validée')],
        default='en_attente'
    )
    date_limite = models.DateField()

class Meta:
        db_table = "OffreStage"  

@property
def est_expiree(self):
        """Vérifie si la date limite est dépassée."""
        return self.date_limite < timezone.now().date()       