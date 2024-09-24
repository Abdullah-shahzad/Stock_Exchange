from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    CreateUserView,
    CreateStockView,
    CreateTransactionView,
    ListStocksView,
    ListUserTransactionsView,
    ListTransactionsByTimestampView,
    GetUserView,
    GetStockView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='create_user'),
    path('login/', LoginView.as_view(), name='create_user'),
    path('users/', CreateUserView.as_view(), name='create_user'),
    path('users/<str:username>/', GetUserView.as_view(), name='get_user'),
    path('create_stock', CreateStockView.as_view(), name='create_stock'),
    path('stocks/', ListStocksView.as_view(), name='list_stocks'),
    path('stocks/<str:ticker>/', GetStockView.as_view(), name='get_stock'),
    path('transactions/', CreateTransactionView.as_view(), name='create_transaction'),
    path('transactions/<str:username>/', ListUserTransactionsView.as_view(), name='list_user_transactions'),
    path('transactions/<str:username>/<str:start_time>/<str:end_time>/', ListTransactionsByTimestampView.as_view(), name='Transaction_with_timestamp'),
]





