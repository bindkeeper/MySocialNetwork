from rest_framework import serializers
from social_app.models import Profile, Post, Like

from pyhunter import PyHunter
import clearbit

clearbit.key = 'sk_5254c897553cb93a13f006573a91f4d4'


def get_clearbit_data(email):
    response = clearbit.Enrichment.find(email=email, srteam=True)
    return response


hunter = PyHunter('0f66ac4aa297fe341926c8b1113dd001f26fbb82')


def get_email_validity(email):
    h_response = hunter.email_verifier(email)
    return h_response['result']


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())
    likes = serializers.PrimaryKeyRelatedField(many=True, queryset=Like.objects.all())

    class Meta:
        model = Profile
        fields = ['id', 'username', 'validity', "clearbit_data", "posts", "likes"]


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

        email = self.validated_data['email']

        email_validity = get_email_validity(email)
        print(email + " valideitiy is " + email_validity)
        clearbit_data = get_clearbit_data(email)

        user = Profile(
                        username=self.validated_data['username'],
                        email=self.validated_data['email'],
                        clearbit_data=clearbit_data,
                        validity=email_validity
                        )
        user.set_password(password)
        user.save()
        return user


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    text = serializers.CharField(style={'base_template': 'textarea.html'})
    owner = serializers.ReadOnlyField(source='owner.username')
    likes = serializers.PrimaryKeyRelatedField(many=True, queryset=Like.objects.all(), required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'owner', 'likes']

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


class LikeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    post_id = serializers.IntegerField()
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        # enforce only one like per user per post
        post_id = validated_data['post_id']
        likes = Like.objects.filter(post_id=post_id, owner=self.context['request'].user)
        if likes.count() > 0:
            raise serializers.ValidationError({'likes': 'You can like this post only once'})
        return Like.objects.create(**validated_data)
