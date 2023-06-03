from django.db import models


class BlogsAPIModel(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    content = models.TextField(max_length=8000, blank=False, unique=True)
    image = models.ImageField(upload_to="posters/", null=False)
    view_count = models.PositiveBigIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Object (%s) <Title: %s\nContent: %s\nImage: %s>" % \
            (self.pk, self.title, self.content, self.image)

    class Meta:
        indexes = [
            models.Index(fields=['title'])
        ]
