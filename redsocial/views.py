from django.http import HttpResponse
from redsocial.serializers import PostsSerializer, CitySerializer, PersonSerializer
from redsocial.models import Posts, City, Person
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

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def hacerPost(request):
    return HttpResponse('<form action="http://192.168.68.137:8000/redsocial/Posts/" method="POST">\
                <div>\
                    <label for="text">Texto de post</label>\
                    <input name="text" id="text" value="text">\
                </div>\
                <div>\
                    <label for="user">usuario</label>\
                    <input name="user" id="user" value="user">\
                </div>\
                <div>\
                    <button>Send my greetings</button>\
                </div>\
                </form>')

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