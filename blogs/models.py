from django.db import models


class BlogsAPIModel(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    content = models.TextField(max_length=8000, blank=False, unique=True)
    image = models.ImageField(upload_to="posters/", null=False)
    date = models.DateTimeField(auto_now_add=True)
