from rest_framework import serializers
from rest_framework.authtoken.admin import User

from .models import Applications


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class OutgoingSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='friend')

    class Meta:
        model = Applications
        fields = ('id', 'user')


class IncomingSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='owner')

    class Meta:
        model = Applications
        fields = ('id', 'user')


class FriendSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='owner')

    class Meta:
        model = Applications
        fields = ('id', 'user')


class ApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applications
        fields = ('id', 'owner_id', 'friend_id',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        owner_id = validated_data['owner_id']
        friend_id = validated_data['friend_id']
        application = Applications.objects.create(
            owner_id=owner_id,
            friend_id=friend_id,
        )
        application.save()
        return application
