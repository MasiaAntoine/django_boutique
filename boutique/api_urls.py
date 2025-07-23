from django.urls import path
from . import api_views

app_name = 'boutique_api'

urlpatterns = [
    # API endpoints
    path('status/', api_views.api_status, name='api_status'),
    path('commandes/export/csv/', api_views.export_commandes_csv, name='export_commandes_csv'),
    path('commandes/import/csv/', api_views.import_commandes_csv, name='import_commandes_csv'),
]
