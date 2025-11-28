from django.shortcuts import render
from .models import Post, User, Category, Tag, Comment
from .serializers import (
        PostSerializer, CategorySerializer, TagSerializer, 
        CommentSerializer, UserSerializer
    )
from rest_framework import viewsets, filters
from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly, IsAdminOrCreateOnlyOrReadOnly
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import get_statistics


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author', 'category').prefetch_related('tags').all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    permission_classes = [IsAuthorOrReadOnly]
    search_fields = ['title', 'content', 'author__username']
    filterset_fields = ['author', 'created_at']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @method_decorator(cache_page(60 * 3))
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        posts_data = response.data.get('results', response.data)

        for post in posts_data:
            content = post.get('content', '')
            if len(content) > 70:
                post['content'] = content[:70] + '...'

        return response

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    pagination_class = None
    permission_classes = [IsAdminOrReadOnly]
    
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    pagination_class = None
    permission_classes = [IsAdminOrCreateOnlyOrReadOnly]
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author', 'post').all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'author']
    permission_classes = [IsAuthorOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @method_decorator(cache_page(60 * 3))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    permission_classes = [permissions.IsAdminUser]


@api_view(['GET'])
def dashboard_view(request):
    stats = get_statistics()
    user = request.user
    user_data = {}
    if user.is_authenticated:
        user_data = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name
        }

    data = {
        'stats': stats,
        'me': user_data
    }
    return Response(data)