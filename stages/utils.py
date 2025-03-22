from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse

def generer_pdf_convention(etudiant, entreprise, encadrant, date_debut, date_fin):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, f"Convention de Stage: {etudiant.nom} {etudiant.prenom}")
    c.drawString(100, 730, f"Entreprise: {entreprise.nom}")
    c.drawString(100, 710, f"Encadrant: {encadrant.nom}")
    c.drawString(100, 690, f"Date de début: {date_debut}")
    c.drawString(100, 670, f"Date de fin: {date_fin}")
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer

def generer_pdf_attestation(etudiant, entreprise, statut):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, f"Attestation de Stage")
    c.drawString(100, 730, f"Etudiant: {etudiant.nom} {etudiant.prenom}")
    c.drawString(100, 710, f"Entreprise: {entreprise.nom}")
    c.drawString(100, 690, f"Statut: {statut}")
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer

def generer_pdf_convocation(etudiant, date_soutenance, lieu_soutenance):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, f"Convocation à la Soutenance")
    c.drawString(100, 730, f"Etudiant: {etudiant.nom} {etudiant.prenom}")
    c.drawString(100, 710, f"Date de Soutenance: {date_soutenance}")
    c.drawString(100, 690, f"Lieu: {lieu_soutenance}")
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer
