from system.models.organization import Post
from core.api import serializer_for
from system.views import ResourceViewSet

class PostViewSet(ResourceViewSet):
    queryset = Post.objects.all()
    serializer_class = serializer_for(Post)
