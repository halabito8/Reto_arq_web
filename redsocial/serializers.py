from rest_framework import serializers

from .models import Posts, Comments

class CommentsSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField()

    class Meta: 
        model = Comments
        fields = '__all__'

class PostsSerializer(serializers.ModelSerializer):
    comments = serializers.ListField(child=serializers.CharField())
    # date = serializers.DateTimeField()

    class Meta:
        model = Posts
        fields = ['_id','user','username', 'text','comments']
