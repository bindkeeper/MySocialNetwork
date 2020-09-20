from rest_framework import serializers
from social_app.models import Profile, Post


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


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    text = serializers.CharField(style={'base_template': 'textarea.html'})
    owner = serializers.ReadOnlyField(source='owner.username')
    #TODO : add likes field

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'owner']

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance