# Generated by Django 4.2.5 on 2023-09-14 03:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='like',
            field=models.IntegerField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='feedcomment',
            name='content',
            field=models.TextField(max_length=256),
        ),
        migrations.AlterField(
            model_name='feedcomment',
            name='feed',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='feed.feed'),
        ),
    ]
