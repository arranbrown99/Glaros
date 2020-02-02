from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/update-stock-prices/', views.update_stock_prices, name='ajax_update_stock_prices'),
    path('ajax/update_migration_timeline/', views.update_migration_timeline, name='ajax_update_migration_timeline'),
]
