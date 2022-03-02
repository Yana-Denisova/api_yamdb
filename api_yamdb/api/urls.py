from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import send_auth_token, send_confirmation_code, UserViewSet, GenresViewSet, CategoriesViewSet, TitleViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)
router_v1.register('genres', GenresViewSet)
router_v1.register('categories', CategoriesViewSet)
router_v1.register('titles', TitleViewSet)

auth_urls = [
    path('signup/', send_confirmation_code, name='send_confirmation_code'),
    path('token/', send_auth_token, name='send_token')
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(router_v1.urls)),
]
