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


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class UserFullInfoSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AuthorSerializer(ModelSerializer):
    user = UserReadOnlyField(read_only=True)

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
