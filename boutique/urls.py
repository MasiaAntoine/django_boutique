from django.urls import path

from . import views

app_name = 'boutique'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('article/<int:article_id>/', views.article_detail_view, name='article_detail'),
    path('categorie/<int:categorie_id>/', views.categorie_view, name='categorie'),
    path('panier/', views.panier_view, name='panier'),
    path('panier/ajouter/<int:article_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/modifier/<int:item_id>/', views.modifier_panier, name='modifier_panier'),
    path('panier/supprimer/<int:item_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),
    path('commander/', views.commander, name='commander'),
    path('compte/', views.compte_client, name='compte_client'),
    path('commandes/', views.mes_commandes, name='mes_commandes'),
    path('commande/<str:numero_commande>/', views.detail_commande, name='detail_commande'),
]
