from rest_framework import serializers

from app1.models import Post, PostPoint


class PostSeriallizers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields='__all__'


class PostPointSeriallizers(serializers.ModelSerializer):
    class Meta:
        model = PostPoint
        fields = '__all__'