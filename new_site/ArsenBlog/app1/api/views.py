from  rest_framework import viewsets
from .serializers import PostSeriallizers, PostPointSeriallizers
from app1.models import Post, PostPoint

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSeriallizers

class PostPointViewSet(viewsets.ModelViewSet):
    queryset = PostPoint.objects.all()
    serializer_class = PostPointSeriallizers