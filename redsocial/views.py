from django.http import HttpResponse
from redsocial.serializers import PostsSerializer, CitySerializer, PersonSerializer
from redsocial.models import Posts, Person
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# para checar si fue creado 
# mongo objeto.pk
# try:
#      from_db = Posts.objects.get(pk=po.pk)
#      return success
#  except Posts.DoesNotExist:
#      return no_success
# neo4j 
# if hasattr(p, 'id'):
#     return success
# else:
#     return no_success

class allPosts(APIView):

    def get(self, request, format=None):
        query = Posts.objects.all()
        serializer = PostsSerializer(query,many=True)
        return Response(serializer.data)

class singlePosts(APIView):

    def get(self, request, format=None):
        p = Posts.objects.filter(user=user)
        serializer = PostsSerializer(p,many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        text = request.data['text']
        user=request.data['user']
        p = Posts(text=text,user=user)
        p.save()
        query = Posts.objects.get(text=text)
        if (query):
            content = {'post': 'creado'}
            return Response(content,status=status.HTTP_200_OK)
        content = {'post': 'no creado'}
        return (content)

    def delete(self, request, format=None):
        p = Posts.objects.filter(user=user)
        for i in p:
            i.delete()
        content = {'post': 'eliminado'}
        return Response(content,status=status.HTTP_200_OK)

class allCities(APIView):

    def get(self, request, format=None):
        query = City.nodes.all()
        serializer = CitySerializer(query,many=True)
        return Response(serializer.data)

class singlePerson(APIView):

    def post(self, request, format=None):
        name=request.data['name']
        age=request.data['age']
        p = Person(name=name,age=age)
        p.save()
        content = {'Persona': 'creada'}
        return Response(content,status=status.HTTP_200_OK)

class allPerson(APIView):

    def get(self, request, format=None):
        p = Person.nodes.all()
        serializer = PersonSerializer(p,many=True)
        return Response(serializer.data)