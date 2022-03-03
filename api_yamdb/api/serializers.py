from rest_framework import serializers

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
    
    class Meta:
        fields = ('name', 'slug')
        read_only_fields = ('id',)
        model = Genres


class CategoriesSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('name', 'slug')
        read_only_fields = ('id',)
        model = Categories

class СategorySerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(
        queryset = Categories.objects.all(),
        slug_field='name')

    class Meta:
        model = Categories
        fields = ('name',)
        read_only_fields = ('id',)

class TitlesGetSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)
    
    class Meta():
        fields = '__all__'
        read_only_fields = ('id',)
        model = Titles

class TitlesPostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug',
    )

    class Meta:
        fields = '__all__'
        model = Titles
