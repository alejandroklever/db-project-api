from collections import OrderedDict

from rest_framework import serializers
from rest_framework.authtoken.models import Token

import apps.revista_cientifica.models as models


class CustomRelatedField(serializers.RelatedField):
    representation_fields = []

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        d = value.__dict__
        return {field: d[field] for field in self.representation_fields}


class ArticleRelatedField(CustomRelatedField):
    representation_fields = ['id', 'title', 'keywords', 'evaluation', 'end_date']


class AuthorRelatedField(CustomRelatedField):
    representation_fields = ['id', 'institution', 'orcid']


class RefereeRelatedField(AuthorRelatedField):
    representation_fields = ['id']


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)
    email = serializers.EmailField(max_length=200)
    orcid = serializers.IntegerField()
    institution = serializers.CharField(max_length=200)

    def create(self, validated_data):
        user = models.User.objects.create_user(username=validated_data['username'],
                                               email=validated_data['email'],
                                               password=validated_data['password'])
        Token.objects.create(user=user)
        models.Author.objects.create(user=user,
                                     orcid=validated_data['orcid'],
                                     institution=validated_data['institution'])
        return user

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def to_representation(self, instance: models.User):
        return OrderedDict(username=instance.username, email=instance.email, password=instance.password,
                           institution=instance.author.institution, orcid=instance.author.orcid)


class UserUpdateSerializer(serializers.ModelSerializer):
    author = AuthorRelatedField(queryset=models.Author.objects.all())
    referee = RefereeRelatedField(queryset=models.Referee.objects.all(), allow_null=True)

    class Meta:
        model = models.User
        fields = ['username', 'email', 'first_name', 'last_name', 'author', 'referee']

    def update(self, instance, validated_data):
        user = instance
        author_data = validated_data.pop('author', None)
        referee_data = validated_data.pop('referee', None)

        user.username = validated_data['username']
        user.email = validated_data['email']
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']

        if author_data:
            user.author.institution = author_data['institution']
            user.author.save()

        if referee_data:
            user.referee = referee_data['speciality']
            user.referee.save()

        user.save()
        return user


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=200)
    new_password = serializers.CharField(max_length=200)

    def create(self, validated_data):
        raise NotImplemented()

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data['password']):
            raise ValueError('Incorrect Password')
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class UserInfoSerializer(serializers.ModelSerializer):
    author = AuthorRelatedField(read_only=True)
    referee = RefereeRelatedField(read_only=True)

    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_superuser', 'author', 'referee']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        exclude = ['articles', ]


class RefereeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Referee
        exclude = ['articles', ]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = '__all__'


class MCCSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MCC
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = '__all__'


class ArticleInReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ArticleInReview
        fields = '__all__'


class ArticleInReviewInfoSerializer(serializers.ModelSerializer):
    article = ArticleRelatedField(read_only=True)
    referee = RefereeRelatedField(read_only=True)

    class Meta:
        model = models.ArticleInReview
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = '__all__'


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Participation
        fields = '__all__'


class ParticipationReadOnlyFieldSerializer(serializers.ModelSerializer):
    author = AuthorRelatedField(read_only=True)
    article = ArticleRelatedField(read_only=True)

    class Meta:
        model = models.Participation
        fields = '__all__'


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'
