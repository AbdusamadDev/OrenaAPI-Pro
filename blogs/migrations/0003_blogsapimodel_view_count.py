# Generated by Django 4.2.1 on 2023-06-03 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_blogsapimodel_blogs_blogs_title_7a2f53_idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogsapimodel',
            name='view_count',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
