from rest_framework.serializers import ModelSerializer, RelatedField

from .models import User, Author, Notification, MCC, Article, File, Participation, Referee, ArticleInReview


class RelationFieldJSONRepresentation(RelatedField):
    representation_fields = []

    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        d = value.__dict__
        return {field: d[field] for field in self.representation_fields}


class UserReadOnlyField(RelationFieldJSONRepresentation):
    representation_fields = ['id', 'username', 'first_name', 'last_name', 'is_superuser']


class UserReadOnlySerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_superuser']
        read_only_fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_superuser']


class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class DetailUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


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


class AuthorSerializer(ModelSerializer):
    user = UserReadOnlyField(read_only=True)

    class Meta:
        model = Author
        fields = '__all__'
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


class ParticipationSerializer(ModelSerializer):
    class Meta:
        model = Participation
        fields = '__all__'


class RefereeSerializer(ModelSerializer):
    class Meta:
        model = Referee
        fields = '__all__'


class ArticleInReviewSerializer(ModelSerializer):
    class Meta:
        model = ArticleInReview
        fields = '__all__'
