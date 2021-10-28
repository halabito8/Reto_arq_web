from rest_framework import serializers

from .models import Posts, City, Person

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['user', 'text']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['code', 'name']

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['age', 'name']