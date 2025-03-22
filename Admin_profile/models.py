from django.contrib.auth.models import User  # type: ignore
from django.db import models

# Modèle pour Filiere
class Filiere(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "filiere"
def __str__(self):
        return self.nom
# Modèle pour Groupe
class Groupe(models.Model):
    nom = models.CharField(max_length=100)

    class Meta:
        db_table = "groupe"
def __str__(self):
        return self.nom  
# Modèle pour Etudiant
class Etudiant(models.Model):
    matricule = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "etudiant"

class Annee(models.Model):
    annee = models.PositiveIntegerField()  

    class Meta:
        db_table = "annee"
class RapportStage(models.Model):
    titre = models.CharField(max_length=255)
    fichier = models.FileField(upload_to='rapports/')  # Sauvegarde dans "media/rapports/"
    date_soumission = models.DateTimeField(auto_now_add=True)
class Meta:
 db_table = "rapports"
