from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from .authentication import Generate_JWT_token, User_authentication, JWT_Required
from .models import Users, Stocks, Transaction
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from stock_exchange_app.serializer import UserSerializer, StockSerializer, TransactionSerializer, registerSerializer, \
    LoginSerializer


@swagger_auto_schema(method='post', request_body=registerSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Handle user registration.
    """
    serializer = registerSerializer(data=request.data)  # Use the serializer to validate data
    if serializer.is_valid():
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        password1 = serializer.validated_data['password']

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password1)  # Hash the password
        )

        # Generate a JWT token for the new user
        token = Generate_JWT_token(user)

        # Return success response with the token
        return Response({"message": "User registered successfully", "token": token}, status=status.HTTP_201_CREATED)

    # Return validation errors if the form is invalid
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=LoginSerializer)
@permission_classes([AllowAny])
@api_view(["POST"])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        return Response({'message': 'Login successful'})
    else:
        return Response({'error': 'Invalid credentials'}, status=401)


@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@JWT_Required
def create_user(request):
    """
    Create a new user with an initial balance.
    """
    serializer = UserSerializer(data=request.data)
    try:
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([AllowAny])
def get_user(request, username):
    """
    Retrieve user data by username.
    """
    user = get_object_or_404(Users, username=username)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=StockSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@JWT_Required
def create_stock(request):
    """
    Create a new stock entry in the database.
    """
    serializer = StockSerializer(data=request.data)
    try:
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([AllowAny])
def list_stocks(request):
    """
    List all available stocks.
    """
    stocks = Stocks.objects.all()
    serializer = StockSerializer(stocks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([AllowAny])
def get_stock(request, ticker):
    """
    Retrieve stock data by ticker.
    """
    stock = get_object_or_404(Stocks, ticker=ticker)
    serializer = StockSerializer(stock)
    return Response(serializer.data, status=status.HTTP_200_OK)



@swagger_auto_schema(method='post', request_body=TransactionSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@JWT_Required
def create_transaction(request):
    """
    Create a new transaction.
    Validate if the user has enough balance (BUY) or add the transaction amount to the user's balance (SELL).
    """
    serializer = TransactionSerializer(data=request.data)
    try:
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            stock = serializer.validated_data['ticker']
            transaction_type = serializer.validated_data['transaction_type']
            volume = serializer.validated_data['transaction_volume']
            price = stock.stock_price * volume

            if transaction_type == 'BUY':
                if user.balance < price:
                    return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
                user.balance -= price

            elif transaction_type == 'SELL':
                user.balance += price

            user.save()
            serializer.save(transaction_price=price)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "An unexpected error occurred: " + str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([AllowAny])
def list_user_transactions(request, username):
    """
    List all transactions for a specific user.
    """
    user = get_object_or_404(Users, username=username)
    transactions = Transaction.objects.filter(user=user)
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='get')
@api_view(['GET'])
def list_transactions_by_timestamp(request, username, start_time, end_time):
    """
    List transactions for a specific user between two timestamps.
    """
    user = get_object_or_404(Users, username=username)

    start_timestamp = parse_datetime(start_time)
    end_timestamp = parse_datetime(end_time)

    if not start_timestamp or not end_timestamp:
        return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

    transactions = Transaction.objects.filter(
        user=user,
        created_time__range=[start_timestamp, end_timestamp]
    )
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
