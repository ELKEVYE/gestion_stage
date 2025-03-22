from django.test import TestCase # type: ignore

# Create your tests here.
# Admin_profile/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail

class PasswordResetTests(TestCase):
    def test_password_reset(self):
        # Créer un utilisateur de test
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')

        # Envoyer une demande de réinitialisation de mot de passe
        response = self.client.post('/password_reset/', {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 200)

        # Vérifier qu'un email a été envoyé
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Réinitialisation de votre mot de passe", mail.outbox[0].subject)