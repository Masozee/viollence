from django.urls import path
from .views import *

urlpatterns = [
    path('incidents/monthly/', MonthlyIncidentCountView.as_view(), name='monthly-incident-count'),
    path('incidents/<str:category_slug>/', IncidentsByCategoryView.as_view(), name='incidents-by-category'),
 #   path('incidents/province/', ProvincialIncidentCountView2, name='incidents-by-province'),
    path('data/<slug:slug>/', DataNameDetailView.as_view(), name='data-name-detail'),
    path('incident-counts/', ProvincialIncidentCountView.as_view(), name='incident-counts'),
    path('incidents-by-category/', MonthlyIncidentCategoryView.as_view(), name='incidents_by_category'),

]

