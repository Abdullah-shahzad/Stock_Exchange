from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_401_UNAUTHORIZED
from .authentication import Generate_JWT_token, JWT_Required
from .models import Users, Stocks, Transaction
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from stock_exchange_app.serializer import UserSerializer, StockSerializer, TransactionSerializer, RegisterSerializer, LoginSerializer


class RegisterView(APIView):
    """
    Handles user registration.

    POST:
    Register a new user. Validates input data, checks for username uniqueness,
    hashes the password, creates a user, and returns a JWT token.
    """

    @permission_classes([AllowAny])
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            password1 = serializer.validated_data['password']

            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password1)
            )

            token = Generate_JWT_token(user)

            return Response({"message": "User registered successfully", "token": token}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Handles user login.

    POST:
    Authenticates the user with username and password, and returns a JWT token.
    """

    @permission_classes([AllowAny])
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            token = Generate_JWT_token(user)

            # Return success response with token
            return Response({
                'message': 'Login successful',
                'token': token
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=HTTP_401_UNAUTHORIZED)


class CreateUserView(APIView):
    """
    Creates a new user. Requires JWT authentication.

    POST:
    Creates a new user with balance information.
    """

    @method_decorator(JWT_Required)
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetUserView(APIView):
    """
    Retrieves user details by username.

    GET:
    Returns the user information including balance.
    """

    @permission_classes([AllowAny])
    @swagger_auto_schema()
    def get(self, request, username):
        user = get_object_or_404(Users, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateStockView(APIView):
    """
    Creates a new stock. Requires JWT authentication.

    POST:
    Creates a new stock with ticker, stock price, and stock name.
    """

    @method_decorator(JWT_Required)
    @swagger_auto_schema(request_body=StockSerializer)
    def post(self, request):
        serializer = StockSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListStocksView(APIView):
    """
    Lists all stocks available in the database.

    GET:
    Returns a list of all stocks.
    """

    @permission_classes([AllowAny])
    @swagger_auto_schema()
    def get(self, request):
        stocks = Stocks.objects.all()
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetStockView(APIView):
    """
    Retrieves stock details by ticker.

    GET:
    Returns the stock information by ticker.
    """

    @permission_classes([AllowAny])
    @swagger_auto_schema()
    def get(self, request, ticker):
        stock = get_object_or_404(Stocks, ticker=ticker)
        serializer = StockSerializer(stock)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateTransactionView(APIView):
    """
    Creates a new transaction for buying or selling stocks. Requires JWT authentication.

    POST:
    Creates a transaction, checks for balance in case of buy, updates user balance accordingly.
    """

    @method_decorator(JWT_Required)
    @swagger_auto_schema(request_body=TransactionSerializer)
    def post(self, request):
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


class ListUserTransactionsView(APIView):
    """
    Lists all transactions for a specific user.

    GET:
    Returns all transactions performed by the specified user.
    """

    @permission_classes([AllowAny])
    @swagger_auto_schema()
    def get(self, request, username):
        user = get_object_or_404(Users, username=username)
        transactions = Transaction.objects.filter(user=user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListTransactionsByTimestampView(APIView):
    """
    Lists all transactions for a user within a specific time range.

    GET:
    Returns transactions by username, filtered by start and end timestamp.
    """

    @permission_classes([AllowAny])
    @swagger_auto_schema()
    def get(self, request, username, start_time, end_time):
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
