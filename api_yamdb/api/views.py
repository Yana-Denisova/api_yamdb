from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend, CharFilter, FilterSet, NumberFilter

from reviews.models import Genres, Categories, Title
from .permissions import IsAdminRole, IsReadOnly
from .serializers import (
    SendCodeSerializer, SendTokenSerializer, UserSerializer,
    GenresSerializer, TitlesPostSerializer, CategoriesSerializer,
    TitlesGetSerializer,
    )

User = get_user_model()
token_generator = PasswordResetTokenGenerator()


@api_view(['POST'])
@permission_classes([AllowAny])
def send_confirmation_code(request):

    serializer = SendCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = request.data.get('email')
    username = request.data.get('username')

    if (User.objects.filter(email=email).exists()
       != User.objects.filter(username=username).exists()):
        content = {'detail': 'Имя не соответствует email'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    user, _ = User.objects.get_or_create(
        email=email,
        username=username
    )

    confirmation_code = token_generator.make_token(user)

    send_mail(
        'YaMDb. Код подтверждения',
        f'Код подтверждения: {confirmation_code}',
        None,
        [email],
        fail_silently=False,
    )

    return Response(
        {'email': email, 'username': username}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_auth_token(request):

    serializer = SendTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)

    confirmation_code = serializer.validated_data.get('confirmation_code')

    if not token_generator.check_token(user, confirmation_code):
        content = {'detail': 'Не верный код подтверждения'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    return Response({'token': str(AccessToken.for_user(user))})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]
    pagination_class = PageNumberPagination
    filterset_fields = ['username']
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def me(self, request, pk=None):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)


class CreateListDeleteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    pass

class GenresViewSet(CreateListDeleteViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [IsReadOnly|IsAdminRole]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'

class CategoriesViewSet(CreateListDeleteViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsReadOnly|IsAdminRole]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class TitlesFilter(FilterSet):
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')
    year = NumberFilter()
    name = CharFilter(lookup_expr='icontains')


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = [IsReadOnly | IsAdminRole]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitlesGetSerializer
        return TitlesPostSerializer
