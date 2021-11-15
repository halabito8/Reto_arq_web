import datetime
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from redsocial.serializers import PostsSerializer, CommentsSerializer
from redsocial.models import Posts, Person, Comments
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from neomodel import db

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

class login(APIView):

    def post(self, request, format=None):
        name = request.data["user"]
        search = Person.nodes.get(name=name)
        print(search)
        return Response({"status": "ok"},status=status.HTTP_200_OK)

class allPosts(APIView):

    def get(self, request, format=None):
        query = Posts.objects.all()
        serializer = PostsSerializer(query,many=True)
        return Response(serializer.data)

class singlePosts(APIView):

    def get(self, request, format=None):
        user=request.data['user']
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
        user=request.data['user']
        p = Posts.objects.filter(user=user)
        for i in p:
            i.delete()
        content = {'post': 'eliminado'}
        return Response(content,status=status.HTTP_200_OK)

class allComments(APIView):

    def get(self, request, format=None):
        query = Comments.objects.all()
        serializer = CommentsSerializer(query,many=True)
        return Response(serializer.data)

class singlePerson(APIView):

    def get(self, request, format=None):
        name=request.data['name']
        person = Person.nodes.filter(name__icontains=name)
        res = []
        for p in person:
            res.append({'name':p.name, 'age': p.age})
        return JsonResponse(res,safe=False)

    def post(self, request, format=None):
        name=request.data['name']
        age=request.data['age']
        p = Person(name=name,age=age)
        p.save()
        content = {'Persona': 'creada'}
        return Response(content,status=status.HTTP_200_OK)

class allPerson(APIView):

    def get(self, request, format=None):
        all_persons = Person.nodes.all()
        res = []
        for p in all_persons:
            res.append({'name':p.name, 'age': p.age,'email':p.email})
        return JsonResponse(res,safe=False)

class friends(APIView):

    def get(self, request, format=None):
        name=request.data['name']
        person = Person.nodes.get(name__icontains=name)
        allfriends = person.friends
        res = []
        for p in allfriends:
            res.append({'name':p.name, 'age': p.age, 'id':p.id})
        return JsonResponse(res,safe=False)

    def post(self, request, format=None):
        _from=request.data['from']
        to = request.data['to']
        p1 = Person.nodes.get_or_none(name=_from)
        p2 = Person.nodes.get_or_none(name=to)
        if p1 is None or p2 is None:
            return JsonResponse({"Una de las dos personas":"no existe"},status=status.HTTP_400_BAD_REQUEST)
        p1.friends.connect(p2)
        return JsonResponse({"relacion":"creada"},safe=False)