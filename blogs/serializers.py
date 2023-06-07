from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser

from blogs.models import BlogsAPIModel

from django.contrib.auth.models import User
from PIL import Image
from dotenv import load_dotenv

load_dotenv()


class BlogsAPISerializer(serializers.ModelSerializer):
    parser_classes = [MultiPartParser]

    class Meta:
        model = BlogsAPIModel
        fields = '__all__'

    def validate_image(self, value):
        image = Image.open(value)
        allowed_extensions = ["jpg", "png", "jpeg"]
        file_extension = value.name.split(".")[-1].lower()
        width, height = image.size

        if file_extension not in allowed_extensions:
            raise ValidationError("Invalid Image extension. Only [jpg, jpeg, png] are accepted")

        if width not in range(500, 1500) and height not in range(100, 500):
            raise ValidationError(
                """
                Invalid image dimensions: %sx%s. Width should be min: 500, 
                max: 1500. Height should be min: 100, max: 500
                """ % (width, height))
        return value


class UserAuthSerializer(serializers.Serializer):
    # class Meta:
    #     model = User
    #     fields = ["username", "password"]
    username = serializers.CharField(max_length=200, allow_null=False)
    password = serializers.CharField(max_length=200, allow_null=False)


