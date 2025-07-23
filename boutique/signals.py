from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

from .models import Commande

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Commande)
def commande_status_changed(sender, instance, **kwargs):
    """
    Signal envoyé avant la sauvegarde d'une commande
    Capture l'ancien statut pour détecter les changements
    """
    if instance.pk:
        try:
            instance._old_status = Commande.objects.get(pk=instance.pk).statut
        except Commande.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Commande)
def commande_validated_notification(sender, instance, created, **kwargs):
    """
    Signal envoyé après la sauvegarde d'une commande
    Envoie une notification quand une commande est validée (confirmée)
    """
    # Si c'est une nouvelle commande ou si le statut a changé vers 'confirmee'
    if (created and instance.statut == 'confirmee') or \
       (hasattr(instance, '_old_status') and 
        instance._old_status != 'confirmee' and 
        instance.statut == 'confirmee'):
        
        # Notification pour les super_users
        notify_superusers_new_order(instance)
        
        # Notification pour le client
        notify_customer_order_confirmed(instance)
        
        logger.info(f"Commande {instance.numero_commande} validée - Notifications envoyées")


def notify_superusers_new_order(commande):
    """
    Notifie tous les super_users qu'une nouvelle commande a été validée
    """
    try:
        # Récupérer tous les super_users
        superusers = User.objects.filter(is_superuser=True, is_active=True)
        
        if not superusers.exists():
            logger.warning("Aucun super_user trouvé pour la notification")
            return
        
        # Sujet et contenu de l'email
        subject = f"🎉 Nouvelle commande validée - {commande.numero_commande}"
        
        # Contexte pour le template
        context = {
            'commande': commande,
            'client': commande.user,
            'total': commande.total,
            'nombre_articles': commande.items.count(),
        }
        
        # Rendu du template HTML
        html_message = render_to_string('emails/commande_validated_admin.html', context)
        plain_message = strip_tags(html_message)
        
        # Envoyer l'email à tous les super_users
        recipient_list = [user.email for user in superusers if user.email]
        
        if recipient_list:
            send_mail(
                subject=subject,
                message=plain_message,
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            logger.info(f"Notification envoyée à {len(recipient_list)} super_users")
        else:
            logger.warning("Aucun email configuré pour les super_users")
            
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de notification aux super_users: {e}")


def notify_customer_order_confirmed(commande):
    """
    Notifie le client que sa commande a été confirmée
    """
    try:
        if not commande.user.email:
            logger.warning(f"Pas d'email configuré pour le client {commande.user.username}")
            return
        
        # Sujet et contenu de l'email
        subject = f"Commande confirmée - {commande.numero_commande}"
        
        # Contexte pour le template
        context = {
            'commande': commande,
            'client': commande.user,
            'items': commande.items.all(),
        }
        
        # Rendu du template HTML
        html_message = render_to_string('emails/commande_confirmed_customer.html', context)
        plain_message = strip_tags(html_message)
        
        # Envoyer l'email au client
        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[commande.user.email],
            fail_silently=False,
        )
        logger.info(f"Confirmation envoyée au client {commande.user.username}")
        
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de confirmation au client: {e}")


@receiver(post_save, sender=Commande)
def log_order_status_change(sender, instance, created, **kwargs):
    """
    Log les changements de statut de commande
    """
    if created:
        logger.info(f"Nouvelle commande créée: {instance.numero_commande} - Statut: {instance.statut}")
    elif hasattr(instance, '_old_status') and instance._old_status != instance.statut:
        logger.info(f"Commande {instance.numero_commande} - Changement de statut: {instance._old_status} → {instance.statut}")
