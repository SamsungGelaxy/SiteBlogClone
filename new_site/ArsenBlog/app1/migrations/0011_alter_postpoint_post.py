# Generated by Django 4.2.11 on 2024-05-19 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_post_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postpoint',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='points', to='app1.post'),
        ),
    ]