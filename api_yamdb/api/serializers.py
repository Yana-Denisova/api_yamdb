from rest_framework import serializers

from datetime import date

from reviews.models import User, Genres, Categories, Titles


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(
    )
    username = serializers.CharField(
        max_length=150,
    )

    def validate_username(self, value):
        if 'me' == value.lower():
            raise serializers.ValidationError(
                'Нельзя создвать пользователя "me"')
        return value


class SendTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField(max_length=128)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role',)
        model = User


class GenresSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(
        queryset = Genres.objects.all(),
        slug_field='name'
    )
    slug = serializers.SlugRelatedField(
        queryset = Genres.objects.all(),
        slug_field='slug'
    )
    
    class Meta:
        fields = ('name', 'slug')
        read_only_fields = ('id',)
        model = Genres


class CategoriesSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(
        queryset = Categories.objects.all(),
        slug_field='name'
    )
    slug = serializers.SlugRelatedField(
        queryset = Categories.objects.all(),
        slug_field='slug'
    )
    
    class Meta:
        fields = ('name', 'slug')
        read_only_fields = ('id',)
        model = Categories


class TitlesSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(
        queryset = Titles.objects.all(),
        slug_field='name')
    today = date.today()
    year = serializers.IntegerField(max_value = int(today.year))
    description = serializers.SlugRelatedField(
        queryset = Titles.objects.all(),
        slug_field='description',
    )
    #categorie = serializers.ChoiceField(choices = )
    #genre = serializers.MultipleChoiceField(choices = )
    
    class Meta:
        fields = '__all__'
        read_only_fields = ('id',)
        model = Titles
