from django.urls import path
from .views import (
    create_user,
    get_user,
    create_stock,
    list_stocks,
    get_stock,
    create_transaction,
    list_user_transactions,
    list_transactions_by_timestamp
)

urlpatterns = [
    path('users/', create_user, name='create_user'),
    path('users/<str:username>/', get_user, name='get_user'),
    path('create_stock', create_stock, name='create_stock'),
    path('stocks/', list_stocks, name='list_stocks'),
    path('stocks/<str:ticker>/', get_stock, name='get_stock'),
    path('transactions/', create_transaction, name='create_transaction'),
    path('transactions/<str:username>/', list_user_transactions, name='list_user_transactions'),
    path('transactions/<str:username>/<str:start_time>/<str:end_time>/', list_transactions_by_timestamp, name='statement'),
]
