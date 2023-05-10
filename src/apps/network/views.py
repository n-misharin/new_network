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


# class Index(APIView):
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (TokenAuthentication,)
#
#     def get(self, request):
#         user = Token.objects.get(key=request.auth.key).user
#         content = {
#             'message': f'Hello, {user.username}! email: {user.email}'
#         }
#         return Response(content)


class AllFriends(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        cur_user = Token.objects.get(key=request.auth.key).user
        out_friends = Applications.objects.filter(owner=cur_user)
        friends = Applications.objects.filter(
            owner_id__in=Subquery(out_friends.values('friend_id')),
            friend_id=cur_user.id,
        )
        return Response({
            "users": str([application.owner.id for application in friends]),
        }, status.HTTP_200_OK)


class InFriends(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user = Token.objects.get(key=request.auth.key).user
        in_result = Applications.objects.filter(friend=user, )
        return Response({
            "users": str([application.owner.id for application in in_result]),
        }, status.HTTP_200_OK)


class OutFriends(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user = Token.objects.get(key=request.auth.key).user
        out_result = Applications.objects.filter(owner=user)
        return Response({
            "users": str([application.friend.id for application in out_result]),
        }, status.HTTP_200_OK)


class Friend(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, username):
        cur_user = Token.objects.get(key=request.auth.key).user
        friend = User.objects.filter(username=username)
        res1 = Applications.objects.filter(owner=cur_user, friend=friend[0])
        res2 = Applications.objects.filter(owner=friend[0], friend=cur_user)

        content = {
            "status": "No friend."
        }

        if len(res1) > 0 and len(res2) > 0:
            content["status"] = "is friend"
        elif len(res1) > 0:
            content["status"] = "outgoing request"
        elif len(res2) > 0:
            content["status"] = "incoming request."

        return Response(content, status.HTTP_200_OK)

    def post(self, request, username):
        cur_user = Token.objects.get(key=request.auth.key).user
        if cur_user.username == username:
            return Response({
                "message": "Friendship request already exists."
            }, status.HTTP_409_CONFLICT)
        friend = User.objects.filter(username=username)
        Applications(owner=cur_user, friend=friend[0]).save()
        return Response({}, status.HTTP_200_OK)

    def delete(self, request, username):
        cur_user = Token.objects.get(key=request.auth.key).user
        friend = User.objects.filter(username=username)
        Applications(owner=cur_user, friend=friend[0]).delete()
        return Response({}, status.HTTP_200_OK)


class CreateUser(APIView):
    def post(self, request):
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            user = serialized.create(request.data)
            # TODO: send token
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmUser(APIView):
    def get(self, request):
        # TODO: ..
        ...
