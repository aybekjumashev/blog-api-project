from django.core.cache import cache
from .models import Post, Comment, User, Tag

def get_statistics():
    stats = cache.get('stats')

    if not stats:
        total_posts = Post.objects.count()
        total_comments = Comment.objects.count()
        total_users = User.objects.count()
        total_tags = Tag.objects.count()
        
        stats = {
            'total_posts': total_posts,
            'total_comments': total_comments,
            'total_users': total_users,
            'total_tags': total_tags
        }
        
        cache.set('stats', stats, 60 * 5)

    return stats