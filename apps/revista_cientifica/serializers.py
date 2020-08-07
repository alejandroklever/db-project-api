from rest_framework.serializers import ModelSerializer

from .models import User, Author, Notification, MCC, Article, File, Participation, Referee, ArticleInReview


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


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
