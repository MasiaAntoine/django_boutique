import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import (Article, Categorie, Commande, CommandeItem, Panier,
                     PanierItem)


def home_view(request):
    """
    Vue de la page d'accueil avec listing des articles
    Affiche les articles avec possibilité de filtrage par catégorie
    """
    # Récupération des paramètres de filtrage
    categorie_id = request.GET.get('categorie')
    recherche = request.GET.get('q', '')

    # Filtrage des articles
    articles = Article.objects.filter(actif=True).select_related('categorie')

    if categorie_id:
        articles = articles.filter(categorie_id=categorie_id)

    if recherche:
        articles = articles.filter(
            Q(nom__icontains=recherche) |
            Q(description__icontains=recherche) |
            Q(description_courte__icontains=recherche)
        )

    # Pagination
    paginator = Paginator(articles, 12)  # 12 articles par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Récupération des catégories pour le menu de filtrage
    categories = Categorie.objects.filter(actif=True).order_by('ordre', 'nom')

    # Articles en vedette
    articles_vedette = Article.objects.filter(actif=True, en_vedette=True)[:6]

    context = {
        'title': 'Boutique en ligne - Accueil',
        'page_obj': page_obj,
        'categories': categories,
        'articles_vedette': articles_vedette,
        'categorie_selectionnee': int(categorie_id) if categorie_id else None,
        'recherche': recherche,
    }

    if request.user.is_authenticated:
        if request.user.is_superuser:
            # Rediriger les super_users vers le dashboard
            return redirect('dashboard:dashboard')
        else:
            context['welcome_message'] = f'Bienvenue {request.user.first_name or request.user.username} ! Découvrez nos produits.'
            # Récupération du panier pour afficher le nombre d'articles
            panier, created = Panier.objects.get_or_create(user=request.user)
            context['panier_total'] = panier.total_articles
    else:
        context['welcome_message'] = 'Bienvenue sur notre boutique en ligne ! Connectez-vous pour commander.'

    return render(request, 'boutique/home.html', context)


def article_detail_view(request, article_id):
    """
    Vue détaillée d'un article
    """
    article = get_object_or_404(Article, id=article_id, actif=True)

    # Articles similaires (même catégorie)
    articles_similaires = Article.objects.filter(
        categorie=article.categorie,
        actif=True
    ).exclude(id=article_id)[:4]

    context = {
        'title': f'{article.nom} - Boutique en ligne',
        'article': article,
        'articles_similaires': articles_similaires,
    }

    if request.user.is_authenticated and not request.user.is_superuser:
        panier, created = Panier.objects.get_or_create(user=request.user)
        context['panier_total'] = panier.total_articles

    return render(request, 'boutique/article_detail.html', context)


def categorie_view(request, categorie_id):
    """
    Vue des articles d'une catégorie spécifique
    """
    categorie = get_object_or_404(Categorie, id=categorie_id, actif=True)

    articles = Article.objects.filter(
        categorie=categorie,
        actif=True
    ).order_by('-created_at')

    # Pagination
    paginator = Paginator(articles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': f'{categorie.nom} - Boutique en ligne',
        'categorie': categorie,
        'page_obj': page_obj,
    }

    if request.user.is_authenticated and not request.user.is_superuser:
        panier, created = Panier.objects.get_or_create(user=request.user)
        context['panier_total'] = panier.total_articles

    return render(request, 'boutique/categorie.html', context)


@login_required
def panier_view(request):
    """
    Vue du panier d'achat
    """
    if request.user.is_superuser:
        return redirect('dashboard:dashboard')

    panier, created = Panier.objects.get_or_create(user=request.user)
    items = panier.items.select_related('article').all()

    context = {
        'title': 'Mon panier - Boutique en ligne',
        'panier': panier,
        'items': items,
    }

    return render(request, 'boutique/panier.html', context)


@login_required
@require_POST
def ajouter_au_panier(request, article_id):
    """
    Ajouter un article au panier
    """
    if request.user.is_superuser:
        return JsonResponse({'error': 'Action non autorisée'}, status=403)

    article = get_object_or_404(Article, id=article_id, actif=True)
    quantite = int(request.POST.get('quantite', 1))

    if article.stock < quantite:
        messages.error(request, f"Stock insuffisant pour {article.nom}")
        return redirect('boutique:article_detail', article_id=article_id)

    panier, created = Panier.objects.get_or_create(user=request.user)

    # Vérifier si l'article est déjà dans le panier
    item, item_created = PanierItem.objects.get_or_create(
        panier=panier,
        article=article,
        defaults={'quantite': quantite, 'prix_unitaire': article.prix_final}
    )

    if not item_created:
        # Mettre à jour la quantité
        nouvelle_quantite = item.quantite + quantite
        if article.stock < nouvelle_quantite:
            messages.error(request, f"Stock insuffisant pour {article.nom}")
        else:
            item.quantite = nouvelle_quantite
            item.save()
            messages.success(request, f"{article.nom} ajouté au panier")
    else:
        messages.success(request, f"{article.nom} ajouté au panier")

    # Retourner en AJAX si demandé
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'panier_total': panier.total_articles,
            'message': f"{article.nom} ajouté au panier"
        })

    return redirect('boutique:panier')


@login_required
@require_POST
def modifier_panier(request, item_id):
    """
    Modifier la quantité d'un article dans le panier
    """
    if request.user.is_superuser:
        return JsonResponse({'error': 'Action non autorisée'}, status=403)

    item = get_object_or_404(PanierItem, id=item_id, panier__user=request.user)
    nouvelle_quantite = int(request.POST.get('quantite', 1))

    if nouvelle_quantite <= 0:
        item.delete()
        messages.success(request, "Article supprimé du panier")
    elif item.article.stock < nouvelle_quantite:
        messages.error(request, f"Stock insuffisant pour {item.article.nom}")
    else:
        item.quantite = nouvelle_quantite
        item.save()
        messages.success(request, "Panier mis à jour")

    return redirect('boutique:panier')


@login_required
@require_POST
def supprimer_du_panier(request, item_id):
    """
    Supprimer un article du panier
    """
    if request.user.is_superuser:
        return JsonResponse({'error': 'Action non autorisée'}, status=403)

    item = get_object_or_404(PanierItem, id=item_id, panier__user=request.user)
    article_nom = item.article.nom
    item.delete()

    messages.success(request, f"{article_nom} supprimé du panier")
    return redirect('boutique:panier')


@login_required
def commander(request):
    """
    Traitement de la commande (paiement fictif)
    """
    if request.user.is_superuser:
        return redirect('dashboard:dashboard')

    panier = get_object_or_404(Panier, user=request.user)

    if not panier.items.exists():
        messages.error(request, "Votre panier est vide")
        return redirect('boutique:panier')

    if request.method == 'POST':
        # Créer la commande
        commande = Commande.objects.create(
            user=request.user,
            total=panier.total_prix,
            adresse_livraison=request.user.profile.address or "Adresse non renseignée",
            telephone=request.user.profile.phone or "Téléphone non renseigné",
            notes=request.POST.get('notes', ''),
            statut='confirmee'
        )

        # Créer les items de commande
        for item in panier.items.all():
            CommandeItem.objects.create(
                commande=commande,
                article_nom=item.article.nom,
                article_description=item.article.description_courte,
                prix_unitaire=item.prix_unitaire,
                quantite=item.quantite,
                sous_total=item.sous_total
            )

            # Décrémenter le stock
            article = item.article
            article.stock -= item.quantite
            article.save()

        # Vider le panier
        panier.vider()

        messages.success(request, f"Commande {commande.numero_commande} confirmée ! Merci pour votre achat.")
        return redirect('boutique:detail_commande', numero_commande=commande.numero_commande)

    context = {
        'title': 'Finaliser la commande - Boutique en ligne',
        'panier': panier,
    }

    return render(request, 'boutique/commander.html', context)


@login_required
def compte_client(request):
    """
    Page compte client
    """
    if request.user.is_superuser:
        return redirect('dashboard:dashboard')

    # Dernières commandes
    dernieres_commandes = request.user.commandes.all()[:5]

    # Calcul du total dépensé
    from django.db.models import Sum
    total_depense = request.user.commandes.aggregate(total=Sum('total'))['total'] or 0

    context = {
        'title': 'Mon compte - Boutique en ligne',
        'dernieres_commandes': dernieres_commandes,
        'total_depense': total_depense,
    }

    return render(request, 'boutique/compte_client.html', context)


@login_required
def mes_commandes(request):
    """
    Liste des commandes du client
    """
    if request.user.is_superuser:
        return redirect('dashboard:dashboard')

    commandes = request.user.commandes.all()

    # Pagination
    paginator = Paginator(commandes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Mes commandes - Boutique en ligne',
        'page_obj': page_obj,
    }

    return render(request, 'boutique/mes_commandes.html', context)


@login_required
def detail_commande(request, numero_commande):
    """
    Détail d'une commande
    """
    if request.user.is_superuser:
        return redirect('dashboard:dashboard')

    commande = get_object_or_404(
        Commande,
        numero_commande=numero_commande,
        user=request.user
    )

    context = {
        'title': f'Commande {commande.numero_commande} - Boutique en ligne',
        'commande': commande,
    }

    return render(request, 'boutique/detail_commande.html', context)
