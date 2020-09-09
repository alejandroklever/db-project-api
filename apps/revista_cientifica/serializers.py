from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer, RelatedField

from .models import (User, Author, Notification, MCC, Article, File, Participation, Referee, ArticleInReview)


class RelatedFieldJSONRepresentation(RelatedField):
    representation_fields = []

    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        d = value.__dict__
        return {field: d[field] for field in self.representation_fields}


class UserRelatedField(RelatedFieldJSONRepresentation):
    representation_fields = ['id', 'username', 'first_name', 'last_name', 'is_superuser']


class ArticleRelatedField(RelatedFieldJSONRepresentation):
    representation_fields = ['id', 'title', 'keywords', 'evaluation', 'end_date']


class AuthorRelatedField(RelatedFieldJSONRepresentation):
    representation_fields = ['id', 'institution', 'orcid']


class RefereeRelatedField(AuthorRelatedField):
    representation_fields = ['id', 'speciality']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class UserReadOnlySerializer(ModelSerializer):
    author = AuthorRelatedField(read_only=True)
    referee = RefereeRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_superuser', 'author', 'referee']


class DetailUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', ]


class UpdateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def update(self, instance, validated_data):
        user = instance
        user.username = validated_data['username']
        user.set_password(validated_data['password'])
        user.email = validated_data['email']
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()
        user.password = ''
        return user


class LoginUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']


class AuthorSerializer(ModelSerializer):
    user = UserRelatedField(read_only=True)

    class Meta:
        model = Author
        exclude = ['articles', ]


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class MCCSerializer(ModelSerializer):
    class Meta:
        model = MCC
        fields = '__all__'


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class FileSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class ParticipationReadOnlyFieldSerializer(ModelSerializer):
    author = AuthorRelatedField(read_only=True)
    article = ArticleRelatedField(read_only=True)

    class Meta:
        model = Participation
        fields = '__all__'


class ParticipationSerializer(ModelSerializer):
    class Meta:
        model = Participation
        fields = '__all__'


class RefereeSerializer(ModelSerializer):
    class Meta:
        model = Referee
        fields = '__all__'


class ArticleInReviewReadOnlyFieldSerializer(ModelSerializer):
    article = ArticleRelatedField(read_only=True)
    referee = RefereeRelatedField(read_only=True)

    class Meta:
        model = ArticleInReview
        fields = '__all__'


class ArticleInReviewSerializer(ModelSerializer):
    class Meta:
        model = ArticleInReview
        fields = '__all__'


class TokenSerializer(ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'
