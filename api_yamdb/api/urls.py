from django.urls import path, include
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
# router.register(
#     r'^titles/(?P<title_id>\d+)/reviews',
#     ReviewViewSet,
#     basename='review'
#     )
# router.register(
#     r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet,
#     basename='comment'
# )

urlpatterns = [
    path('', include(router.urls))
]
