# Generated by Django 4.2.11 on 2024-06-02 07:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app1', '0012_postpoint_date_uploaded_postpoint_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dislike',
            field=models.ManyToManyField(blank=True, related_name='unlike', to=settings.AUTH_USER_MODEL),
        ),
    ]
