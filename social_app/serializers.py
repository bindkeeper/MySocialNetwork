from rest_framework import serializers
from social_app.models import Profile


class UserSerializer(serializers.ModelSerializer):
    #TODO add posts and likes fields

    class Meta:
        model = Profile
        fields = ['id', 'username', 'validity', "clearbit_data"]


class UserCreateSerializer(serializers.ModelSerializer):

    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'password', 'password_confirm']
        extra_kwargs = {
                        'password': {'write_only': True},
                        'password_confirm': {'write_only': True},
                        }

    def save(self):
        password = self.validated_data['password']
        password_confirm = self.validated_data['password_confirm']
        if password != password_confirm:
            raise serializers.ValidationError({'password': 'passwords must match'})

        # TODO add verifier

        user = Profile(
                        username=self.validated_data['username'],
                        email=self.validated_data['email']
                        )
        user.set_password(password)
        user.save()
        return user
