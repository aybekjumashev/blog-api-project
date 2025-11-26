from django.urls import path
from .views import PostViewSet, CategoryViewSet, TagViewSet, CommentViewSet, UserViewSet, dashboard_view
from rest_framework.routers import DefaultRouter, SimpleRouter

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'comments', CommentViewSet, basename='comment')

router.register(r'users', UserViewSet, basename='user')

urlpatterns = router.urls

urlpatterns += [
    path('dashboard/', dashboard_view, name='dashboard'),
]