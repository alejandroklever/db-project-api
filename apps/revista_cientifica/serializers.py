from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer, RelatedField, CharField, IntegerField

from .models import User, Author, Notification, MCC, Article, File, Participation, Referee, ArticleInReview


class CustomRelatedField(RelatedField):
    representation_fields = []

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        d = value.__dict__
        return {field: d[field] for field in self.representation_fields}


class ArticleRelatedField(CustomRelatedField):
    representation_fields = ['id', 'title', 'keywords', 'evaluation', 'end_date']


class AuthorRelatedField(CustomRelatedField):
    representation_fields = ['id', 'profile_image_url', 'institution', 'orcid']


class RefereeRelatedField(AuthorRelatedField):
    representation_fields = ['id', 'speciality']


class UserCreateSerializer(ModelSerializer):
    orcid = IntegerField()
    institution = CharField(max_length=200)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'orcid', 'institution']

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        email=validated_data['email'],
                                        password=validated_data['password'])
        Token.objects.create(user=user)
        Author.objects.create(user=user,
                              orcid=validated_data['orcid'],
                              institution=validated_data['institution'])
        return user


class UserUpdateSerializer(ModelSerializer):
    author = AuthorRelatedField(queryset=Author.objects.all())
    referee = RefereeRelatedField(queryset=Referee.objects.all(), allow_null=True)

    class Meta:
        model = User
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


class UserInfoSerializer(ModelSerializer):
    author = AuthorRelatedField(read_only=True)
    referee = RefereeRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_superuser', 'author', 'referee']


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        exclude = ['articles', ]


class RefereeSerializer(ModelSerializer):
    class Meta:
        model = Referee
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


class ArticleInReviewSerializer(ModelSerializer):
    class Meta:
        model = ArticleInReview
        fields = '__all__'


class ArticleInReviewInfoSerializer(ModelSerializer):
    article = ArticleRelatedField(read_only=True)
    referee = RefereeRelatedField(read_only=True)

    class Meta:
        model = ArticleInReview
        fields = '__all__'


class FileSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class ParticipationSerializer(ModelSerializer):
    class Meta:
        model = Participation
        fields = '__all__'


class ParticipationReadOnlyFieldSerializer(ModelSerializer):
    author = AuthorRelatedField(read_only=True)
    article = ArticleRelatedField(read_only=True)

    class Meta:
        model = Participation
        fields = '__all__'


class TokenSerializer(ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'
