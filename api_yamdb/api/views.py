from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .mixins import CreateListDeleteViewSet
from reviews.models import Category, Genre, Review, Title, User
from .filters import TitlesFilter
from .permissions import AuthorAdminModerOrReadOnly, IsAdminRole, IsReadOnly
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenresSerializer, ReviewSerializer,
                          SendCodeSerializer, SendTokenSerializer,
                          TitlesGetSerializer, TitlesPostSerializer,
                          UserSerializer)

token_generator = PasswordResetTokenGenerator()


@api_view(['POST'])
@permission_classes([AllowAny])
def send_confirmation_code(request):
    serializer = SendCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    user, _ = User.objects.get_or_create(
        email=email,
        username=username)
    confirmation_code = token_generator.make_token(user)
    send_mail(
        'YaMDb. Код подтверждения',
        f'Код подтверждения: {confirmation_code}',
        None,
        [email],
        fail_silently=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_auth_token(request):
    serializer = SendTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.validated_data.get('confirmation_code')
    if not token_generator.check_token(user, confirmation_code):
        return Response(
            {'detail': 'Не верный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST)
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
        permission_classes=[IsAuthenticated])
    def me(self, request, pk=None):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)


class GenresViewSet(CreateListDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [IsReadOnly | IsAdminRole]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class CategoriesViewSet(CreateListDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsReadOnly | IsAdminRole]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    permission_classes = [IsReadOnly | IsAdminRole]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitlesGetSerializer
        return TitlesPostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title_id.reviews.all()

    def perform_create(self, serializer):
        title_id = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorAdminModerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)
