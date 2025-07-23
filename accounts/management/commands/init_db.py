from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import Profile


class Command(BaseCommand):
    """
    Commande Django pour initialiser la base de données
    Usage: python manage.py init_db
    """
    help = 'Supprime toutes les données et crée les comptes par défaut'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirme la suppression des données sans demander',
        )

    def handle(self, *args, **options):
        """
        Point d'entrée de la commande
        """
        self.stdout.write(
            self.style.WARNING('🚀 Initialisation de la base de données')
        )
        self.stdout.write('=' * 50)

        # Demander confirmation si --confirm n'est pas utilisé
        if not options['confirm']:
            confirm = input(
                '⚠️  Cette action va supprimer TOUTES les données. '
                'Êtes-vous sûr ? (oui/non): '
            )
            if confirm.lower() not in ['oui', 'o', 'yes', 'y']:
                self.stdout.write(
                    self.style.ERROR('❌ Opération annulée.')
                )
                return

        # Exécuter l'initialisation
        if self.clear_database() and self.create_users():
            self.display_success_message()
        else:
            self.stdout.write(
                self.style.ERROR('❌ Échec de l\'initialisation.')
            )

    def clear_database(self):
        """
        Supprime toutes les données de la base de données
        """
        self.stdout.write('🗑️  Suppression de toutes les données...')

        try:
            with transaction.atomic():
                User.objects.all().delete()
                self.stdout.write(
                    self.style.SUCCESS('✅ Toutes les données supprimées')
                )
                return True
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erreur suppression : {e}')
            )
            return False

    def create_users(self):
        """
        Crée les utilisateurs par défaut
        """
        success = True

        # Créer l'admin
        if self.create_admin_user():
            self.stdout.write(
                self.style.SUCCESS('✅ Compte admin créé')
            )
        else:
            success = False

        # Créer le client
        if self.create_client_user():
            self.stdout.write(
                self.style.SUCCESS('✅ Compte client créé')
            )
        else:
            success = False

        return success

    def create_admin_user(self):
        """
        Crée le compte administrateur
        """
        try:
            admin = User.objects.create_user(
                username='admin',
                email='admin@boutique.com',
                password='1234@',
                first_name='Admin',
                last_name='Boutique',
                is_staff=True,
                is_superuser=True
            )

            admin.profile.is_client = False
            admin.profile.save()

            return True

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erreur création admin : {e}')
            )
            return False

    def create_client_user(self):
        """
        Crée le compte client
        """
        try:
            User.objects.create_user(
                username='client',
                email='client@boutique.com',
                password='1234',
                first_name='Client',
                last_name='Test',
                is_staff=False,
                is_superuser=False
            )

            return True

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erreur création client : {e}')
            )
            return False

    def display_success_message(self):
        """
        Affiche le message de succès
        """
        self.stdout.write('')
        self.stdout.write('=' * 50)
        self.stdout.write(
            self.style.SUCCESS('🎉 Initialisation terminée avec succès !')
        )
        self.stdout.write('')
        self.stdout.write('📋 Comptes créés :')
        self.stdout.write('   👑 Admin:')
        self.stdout.write('      Email    : admin@boutique.com')
        self.stdout.write('      Password : 1234@')
        self.stdout.write('      Type     : Superuser')
        self.stdout.write('')
        self.stdout.write('   👤 Client:')
        self.stdout.write('      Email    : client@boutique.com')
        self.stdout.write('      Password : 1234')
        self.stdout.write('      Type     : Client')
        self.stdout.write('')
        self.stdout.write(
            '🌐 Lancez le serveur avec : python manage.py runserver'
        )
