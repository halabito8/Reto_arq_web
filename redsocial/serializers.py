from rest_framework import serializers

from .models import Posts, Comments

class CommentsSerializer2(serializers.ModelSerializer):
    date = serializers.DateTimeField()

    class Meta: 
        model = Comments
        fields = ['comment','user','username','date']

class CommentsSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField()

    class Meta: 
        model = Comments
        fields = '__all__'

class PostsSerializer(serializers.ModelSerializer):
    comments = CommentsSerializer2(many=True)
    # date = serializers.DateTimeField()

    class Meta:
        model = Posts
        fields = ['_id','user','username', 'text','comments']
