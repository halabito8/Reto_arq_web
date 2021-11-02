from rest_framework import serializers

from .models import Posts, Person

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['user', 'text']

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['age', 'name']