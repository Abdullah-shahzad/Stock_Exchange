import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response


def Generate_JWT_token(user):
    """
    Generates a JWT token for the given user.
    :param user: The User object for which the token is generated.
    :return: JWT token as a string.
    """
    payload = {
        'id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SIMPLE_JWT['SIGNING_KEY'], algorithm=settings.SIMPLE_JWT['ALGORITHM'])
    return token



def User_authentication(username,  password):
    """
    Authenticates the user and returns a JWT token if authentication is successful.
    :param username: Username of the user trying to authenticate.
    :param password: Password of the user.
    :return: user, JWT token if authenticated, otherwise None.
    """

    user = authenticate(username=username, password=password)
    if user is None:
        return None
    else:
        token = Generate_JWT_token(user)
        return user, token




def Decode_JWT_token(token):
    """
        Decodes the JWT token and returns the user if the token is valid.
        :param token: The JWT token to decode.
        :return: User object if the token is valid.
        :raises: AuthenticationFailed if the token is invalid or expired.
    """

    try:
        payload = jwt.decode(token, settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
        user = User.objects.get(id=payload['id'])
        return user
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token has expired. Please log in again.')
    except jwt.DecodeError:
        raise AuthenticationFailed('Invalid token. Token could not be decoded.')
    except User.DoesNotExist:
        raise AuthenticationFailed('User not found for this token.')




def JWT_Required(view_func):
    """
    Decorator to protect views that require JWT authentication.
    :param view_func: The view function to wrap with authentication logic.
    :return: The wrapped function with JWT validation.
    """
    def wrapper(request, *args, **kwargs):
        # Retrieve the Authorization header
        auth_header = request.headers.get('Authorization')
        print(auth_header)  # Debugging - prints the auth header for inspection

        # If no Authorization header is present
        if not auth_header:
            return Response({'error': 'Token not found.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Ensure the Authorization header is in the expected 'Bearer <token>' format
            if 'Bearer' not in auth_header:
                return Response({'error': 'Invalid token format.'}, status=status.HTTP_400_BAD_REQUEST)

            # Extract the token after 'Bearer'
            token = auth_header.split(' ')[1]
            user = Decode_JWT_token(token)  # Your JWT decode function
            request.user = user  # Attach the decoded user to the request

        # Handle expired token exception
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token has expired. Please log in again.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Handle cases where token split fails or token is malformed/invalid
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return Response({'error': 'Token is invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

        # If the token is valid, proceed with the view function
        return view_func(request, *args, **kwargs)

    return wrapper







