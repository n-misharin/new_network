from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User
from django.db.models import Subquery
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
        out_result = Applications.objects.filter(owner=user)
        in_result = Applications.objects.filter(friend=user, )
        friends = Applications.objects.filter(
            friend=user,
            friend_id__in=Subquery(out_result.values('friend_id')),
        )
        return Response({
            "user": user.id,
            "out": str([application.friend.id for application in out_result]),
            "in": str([application.owner.id for application in in_result]),
            "friends": str([application.friend.id for application in friends]),
        }, status.HTTP_200_OK)


class AddFriend(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, username):
        cur_user = Token.objects.get(key=request.auth.key).user
        friend = User.objects.filter(username=username)
        Applications(owner=cur_user, friend=friend[0]).save()
        return Response({}, status.HTTP_200_OK)


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
    def get(self, request):
        for user in User.objects.all():
            user.staff_status = True
            user.save()
        # TODO: ..
