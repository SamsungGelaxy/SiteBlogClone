from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from slugify import slugify
# Create your models here.
class PublicManager(models.Manager):
    def get_queryset(self):
            return super().get_queryset().filter(status="published")

class Post(models.Model):
    STATUS_CHOISES=(("draft", "Draft"), ("published", "Published"),)
    like=models.ManyToManyField(User, related_name="like_p", blank=True)


    title=models.CharField(max_length=30, verbose_name="Title")

    tag=TaggableManager(blank=True)

    slug=models.SlugField(unique_for_date="publish")

    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name="post", verbose_name="Author", default=None)

    short_des=models.CharField(max_length=255, verbose_name="Description")
    publish=models.DateTimeField(default=timezone.now, verbose_name="Publish")
    date_create=models.DateTimeField(auto_now_add=True, verbose_name="Create_date")
    date_update=models.DateTimeField(auto_now=True, verbose_name="Update_date")

    objects=models.Manager()
    public=PublicManager()
    status=models.CharField(verbose_name="status", choices=STATUS_CHOISES, default="draft", max_length=255)

    img=models.ImageField(
        verbose_name="picture",
        upload_to="pictures/",
        blank=False,
    )

    class Meta:
        ordering=["-publish",]
        indexes = [
            models.Index(fields=["-publish"]),
        ]


    def __str__(self):
        return f"Post.{self.pk}"

    def get_absolute_url(self):

        return reverse("app1:post_detail", args=(self.publish.year, self.publish.month, self.publish.day, self.slug,))
    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        return super(Post, self).save(args, kwargs)

def save_img(instance, filename):
    post_id=instance.post.id
    return "pictures/{}/{}".format(post_id, filename)

class PostPoint(models.Model):
    header=models.CharField(max_length=30, verbose_name="Header", default="Title")
    post=models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    post_point_text=models.TextField(verbose_name="Post_point")
    post_img = models.ImageField(
        verbose_name="picture_point",
        upload_to=save_img,
        blank=True,
    )

    def __str__(self):
        return "Post_point.{}".format(self.post.title)

class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE, default=None, related_name="comments")
    name=models.CharField(max_length=30, verbose_name="Title")
    emeil=models.EmailField()
    text = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Create_date")
    date_update = models.DateTimeField(auto_now=True, verbose_name="Update_date")
    active=models.BooleanField(default=True)
    class Meta:
        ordering=["-date_create",]
        indexes = [
            models.Index(fields=["-date_create"]),
        ]
    def __str__(self):
        return f"Comment.{self.pk}"
