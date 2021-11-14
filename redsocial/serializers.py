from rest_framework import serializers

from .models import Posts, Person

class PostsSerializer(serializers.ModelSerializer):
    comments = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Posts
        fields = ['user', 'text','comments','_id']

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['age', 'name']