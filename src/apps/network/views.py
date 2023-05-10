from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from .models import Applications
from .serializers import UserSerializer


class Index(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user = Token.objects.get(key=request.auth.key).user
        content = {
            'message': f'hello {user.username} ({user.email})'
        }
        return Response(content)


class Friends(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user = Token.objects.get(key=request.auth.key).user
        result = Applications.objects.filter(owner=user)
        for i in result:
            print(i)
        return Response({}, status.HTTP_200_OK)


class AddFriend(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, user_id):
        print("!!!!!!!!!!")
        user = Token.objects.get(key=request.auth.key).user
        # friend = User.objects.filter(user_id=user_id)
        # Applications(owner=user, friend=friend)
        return Response({}, status.HTTP_201_CREATED)


class CreateUser(APIView):
    def post(self, request):
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            user = serialized.create(request.data)
            account_activation_token = PasswordResetTokenGenerator().make_token(user)
            return Response({
                'confirm_link': f'http://localhost:8000/confirm/{account_activation_token}/'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmUser(APIView):
    def get(self, request, token):
        # TODO: ..
        ...
