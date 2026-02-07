import re

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def healthcheck(request):
    return Response({'status': 'ok'})


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    User = get_user_model()

    full_name = request.data.get('full_name', '').strip()
    email = request.data.get('email', '').strip().lower()
    password = request.data.get('password', '').strip()
    confirm_password = request.data.get('confirm_password', '').strip()

    errors = {}

    if not full_name:
        errors['full_name'] = 'Full name is required.'
    elif len(full_name) < 2:
        errors['full_name'] = 'Full name must be at least 2 characters.'
    elif not re.fullmatch(r'[A-Za-z ]+', full_name):
        errors['full_name'] = 'Full name can contain only letters and spaces.'

    if not email:
        errors['email'] = 'Email is required.'
    else:
        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = 'Enter a valid email address.'

    if not password:
        errors['password'] = 'Password is required.'
    else:
        if len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters.'
        elif ' ' in password:
            errors['password'] = 'Password cannot contain spaces.'
        elif not re.search(r'[A-Z]', password):
            errors['password'] = 'Password must include at least one uppercase letter.'
        elif not re.search(r'[a-z]', password):
            errors['password'] = 'Password must include at least one lowercase letter.'
        elif not re.search(r'\d', password):
            errors['password'] = 'Password must include at least one number.'

    if not confirm_password:
        errors['confirm_password'] = 'Confirm password is required.'
    elif confirm_password != password:
        errors['confirm_password'] = 'Passwords do not match.'

    if errors:
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    username = email

    if User.objects.filter(email=email).exists():
        return Response(
            {'email': 'Email already registered.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )
    user.first_name = full_name
    user.save(update_fields=['first_name'])

    token, _ = Token.objects.get_or_create(user=user)

    return Response(
        {
            'token': token.key,
            'username': user.username,
            'email': user.email,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    if request.method == 'PUT':
        username = request.data.get('username', '').strip()
        email = request.data.get('email', '').strip()

        if not username or not email:
            return Response(
                {'error': 'Username and email are required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(username) < 3 or len(username) > 30:
            return Response(
                {'error': 'Username must be between 3 and 30 characters.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            UnicodeUsernameValidator()(username)
        except ValidationError:
            return Response(
                {'error': 'Username contains invalid characters.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {'error': 'Enter a valid email address.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            get_user_model()
            .objects
            .filter(username=username)
            .exclude(id=user.id)
            .exists()
        ):
            return Response(
                {'error': 'Username already exists.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            get_user_model()
            .objects
            .filter(email=email)
            .exclude(id=user.id)
            .exists()
        ):
            return Response(
                {'error': 'Email already exists.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.username = username
        user.email = email
        user.save(update_fields=['username', 'email'])

    role = 'Admin' if user.is_staff or user.is_superuser else 'User'
    return Response(
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': role,
            'last_login': user.last_login.isoformat() if user.last_login else None,
        }
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    Token.objects.filter(user=request.user).delete()
    return Response({'detail': 'Logged out.'}, status=status.HTTP_200_OK)


class PublicAuthTokenView(ObtainAuthToken):
    """
    Public login endpoint.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        identifier = request.data.get('username', '').strip()
        password = request.data.get('password', '').strip()
        if not identifier or not password:
            return Response(
                {'error': 'Email/username and password are required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = None
        if '@' in identifier:
            user = (
                get_user_model()
                .objects
                .filter(email__iexact=identifier)
                .first()
            )
            if user:
                identifier = user.username

        user = authenticate(request, username=identifier, password=password)
        if not user or not user.is_active:
            return Response(
                {'error': 'Invalid email or password'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
