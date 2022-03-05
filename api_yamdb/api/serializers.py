from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title, User


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(
        max_length=150)

    def validate_username(self, value):
        if 'me' == value.lower():
            raise serializers.ValidationError(
                'Нельзя создвать пользователя "me"')
        return value

    def validate(self, data):
        if (User.objects.filter(email=data['email']).first()
           != User.objects.filter(username=data['username']).first()):
            raise serializers.ValidationError(
                'Имя не соответствует email')
        return data


class SendTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField(max_length=128)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role')
        model = User


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Genre


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Category


class TitlesGetSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.IntegerField()

    class Meta():
        fields = '__all__'
        read_only_fields = ('id',)
        model = Title


class TitlesPostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True)
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug')

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['view'].request.method == 'POST':
            title_id = self.context['view'].kwargs['title_id']
            if Review.objects.filter(
                title_id=title_id,
                author=self.context['request'].user
            ).exists():
                raise serializers.ValidationError(
                    'На одно произведение можно оставить только один отзыв')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
