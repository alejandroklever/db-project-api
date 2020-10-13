from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer, Serializer, RelatedField, CharField, IntegerField, EmailField

import apps.revista_cientifica.models as models


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
    representation_fields = ['id', 'institution', 'orcid']


class RefereeRelatedField(AuthorRelatedField):
    representation_fields = ['id', 'speciality']


class UserCreateSerializer(Serializer):
    username = CharField(max_length=200)
    password = CharField(max_length=200)
    email = EmailField(max_length=200)
    orcid = IntegerField()
    institution = CharField(max_length=200)

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

    # def to_representation(self, instance: models.User):
    #     return {
    #         'username': instance.username,
    #         'first_name': instance.first_name,
    #         'last_name': instance.last_name,
    #         'email': instance.email,
    #         'is_superuser': instance.is_superuser,
    #         'author': AuthorSerializer(instance.author).data if instance.author is not None else None,
    #         'referee': None
    #     }


class UserUpdateSerializer(ModelSerializer):
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


class UserChangePasswordSerializer(Serializer):
    password = CharField(max_length=200)
    new_password = CharField(max_length=200)

    def create(self, validated_data):
        raise NotImplemented()

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data['password']):
            raise ValueError('Incorrect Password')
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class UserInfoSerializer(ModelSerializer):
    author = AuthorRelatedField(read_only=True)
    referee = RefereeRelatedField(read_only=True)

    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_superuser', 'author', 'referee']


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = models.Author
        exclude = ['articles', ]


class RefereeSerializer(ModelSerializer):
    class Meta:
        model = models.Referee
        exclude = ['articles', ]


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = models.Notification
        fields = '__all__'


class MCCSerializer(ModelSerializer):
    class Meta:
        model = models.MCC
        fields = '__all__'


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = models.Article
        fields = '__all__'


class ArticleInReviewSerializer(ModelSerializer):
    class Meta:
        model = models.ArticleInReview
        fields = '__all__'


class ArticleInReviewInfoSerializer(ModelSerializer):
    article = ArticleRelatedField(read_only=True)
    referee = RefereeRelatedField(read_only=True)

    class Meta:
        model = models.ArticleInReview
        fields = '__all__'


class FileSerializer(ModelSerializer):
    class Meta:
        model = models.File
        fields = '__all__'


class ParticipationSerializer(ModelSerializer):
    class Meta:
        model = models.Participation
        fields = '__all__'


class ParticipationReadOnlyFieldSerializer(ModelSerializer):
    author = AuthorRelatedField(read_only=True)
    article = ArticleRelatedField(read_only=True)

    class Meta:
        model = models.Participation
        fields = '__all__'


class TokenSerializer(ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'
