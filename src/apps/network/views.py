from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User
from django.db.models import Subquery
from rest_framework import permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from .models import Applications
from .serializers import UserSerializer, OutgoingSerializer, IncomingSerializer, ApplicationsSerializer


class OutgoingRequestAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = OutgoingSerializer

    def get_queryset(self):
        cur_user = Token.objects.get(key=self.request.auth.key).user
        return Applications.objects.filter(owner_id=cur_user.id)


class IncomingRequestAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = IncomingSerializer

    def get_queryset(self):
        cur_user = Token.objects.get(key=self.request.auth.key).user
        return Applications.objects.filter(friend_id=cur_user.id)


class AcceptedRequestAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = IncomingSerializer

    def get_queryset(self):
        cur_user = Token.objects.get(key=self.request.auth.key).user
        out_friends = Applications.objects.filter(owner=cur_user)
        return Applications.objects.filter(
            owner_id__in=Subquery(out_friends.values('friend_id')),
            friend_id=cur_user.id,
        )


class FriendAPIView(APIView):
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
                "message": "You can't send yourself a friendship request."
            }, status.HTTP_409_CONFLICT)

        friend = User.objects.filter(username=username)

        if len(friend) == 0:
            return Response({
                "message": "User not found."
            }, status.HTTP_404_NOT_FOUND)

        request_data = {
            "owner_id": cur_user.id,
            'friend_id': friend[0].id,
        }

        application = Applications.objects.filter(
            owner_id=request_data['owner_id'],
            friend_id=request_data['friend_id']
        )

        if len(application) != 0:
            return Response({
                "message": "Friendship request already exists."
            }, status.HTTP_400_BAD_REQUEST)

        serialized = ApplicationsSerializer(data=request_data)

        if serialized.is_valid():
            serialized.create(request_data)
            return Response(serialized.initial_data, status.HTTP_200_OK)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

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
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmUser(APIView):
    def get(self, request):
        # TODO: ..
        ...
