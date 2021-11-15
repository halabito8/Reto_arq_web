import datetime
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from redsocial.serializers import PostsSerializer, CommentsSerializer
from redsocial.models import Posts, Person, Comments
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from neomodel import db
from bson import ObjectId

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
#

class login(APIView):

    def post(self, request, format=None):
        name = request.data["user"]
        search = Person.nodes.get_or_none(name=name)
        if search is None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response({"status": "ok"},status=status.HTTP_200_OK)

class register(APIView):

    def post(self, request, format=None):
        name=request.data['name']
        age=request.data['age']
        email=request.data['email']
        p = Person(name=name,age=age,email=email)
        p.save()
        content = {'Persona': 'creada'}
        return Response(content,status=status.HTTP_200_OK)


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
        userid=request.data['user']
        person = Person.nodes.get_or_none(uid=userid)
        if person is None:
            return Response({"person_id":"no existe"},status=status.HTTP_400_BAD_REQUEST)
        p = Posts(text=text,user=userid,username=person.name)
        p.save()
        try:
            from_db = Posts.objects.get(pk=p.pk)
            content = {'post': 'creado'}
            return Response(content,status=status.HTTP_200_OK)
        except Posts.DoesNotExist:
            content = {'post': 'no creado'}
            return Response(content,status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        id=request.data['id']
        p = Posts.objects.get(_id=ObjectId(id))
        p.text = request.data['text']
        p.save()
        content = {'post': 'modificado'}
        return Response(content,status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        id=request.data['id']
        p = Posts.objects.get(_id=ObjectId(id))
        p.delete()
        content = {'post': 'eliminado'}
        return Response(content,status=status.HTTP_200_OK)

class allComments(APIView):

    def get(self, request, format=None):
        query = Comments.objects.all()
        serializer = CommentsSerializer(query,many=True)
        return Response(serializer.data)
    
class singleComment(APIView):

    def post(self, request, format=None):
        userId=request.data['userId']
        comment=request.data['comment']
        postId = request.data['postId']
        person = Person.nodes.get_or_none(uid=userId)
        if person is None:
            return Response({"person_id":"no existe"},status=status.HTTP_400_BAD_REQUEST)
        p = Posts.objects.get(_id=ObjectId(postId))
        newComment = Comments(user=userId,
                              comment=comment,
                              date=datetime.datetime.now(),
                              username=person.name)
        newComment.save()
        try:
            from_db = Comments.objects.get(pk=newComment.pk)
            content = {'comentario': 'creado'}
            com = p.comments
            if com is None:
                com = [{'_id':newComment._id,
                        'comment':newComment.comment,
                        'user':newComment.user,
                        'date':datetime.datetime.now()}]
            else:
                com.append({'_id':newComment._id,
                            'comment':newComment.comment,
                            'user':newComment.user,
                            'date':datetime.datetime.now()})
            p.comments = com
            p.save()
            return Response(content,status=status.HTTP_200_OK)
        except Comments.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class feed(APIView):

    def get(self, request, format=None):
        id=request.data['id']
        person = Person.nodes.get(uid=id)
        allfriends = person.friends
        res = []
        for p in allfriends:
            res.append(p.uid)
        feed = Posts.objects.filter(user__in=res)
        serializer = PostsSerializer(feed,many=True)
        return Response(serializer.data)


class singlePerson(APIView):

    def get(self, request, format=None):
        id=request.data['id']
        person = Person.nodes.get_or_none(uid=id)
        if person is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'name':p.name, 'age': p.age, 'email':p.email},safe=False,status=status.HTTP_200_OK)


class searchPersons(APIView):

    def get(self, request, format=None):
        name=request.data['name']
        person = Person.nodes.filter(name__icontains=name)
        res = []
        for p in person:
            res.append({'name':p.name, 'age': p.age})
        return JsonResponse(res,safe=False)

class allPerson(APIView):

    def get(self, request, format=None):
        all_persons = Person.nodes.all()
        res = []
        for p in all_persons:
            res.append({'name':p.name, 'age': p.age,'email':p.email, 'id':p.uid})
        return JsonResponse(res,safe=False)

class friends(APIView):

    def get(self, request, format=None):
        id=request.data['id']
        person = Person.nodes.get(uid=id)
        allfriends = person.friends
        res = []
        for p in allfriends:
            res.append({'name':p.name, 'age': p.age, 'id':p.uid})
        return JsonResponse(res,safe=False)

    def post(self, request, format=None):
        _from=request.data['from']
        to = request.data['to']
        p1 = Person.nodes.get_or_none(uid=_from)
        p2 = Person.nodes.get_or_none(uid=to)
        if p1 is None or p2 is None:
            return JsonResponse({"Una de las dos personas":"no existe"},status=status.HTTP_400_BAD_REQUEST)
        p1.friends.connect(p2)
        return JsonResponse({"relacion":"creada"},safe=False)


    def delete(self, request, format=None):
        _from=request.data['from']
        to = request.data['to']
        p1 = Person.nodes.get_or_none(uid=_from)
        p2 = Person.nodes.get_or_none(uid=to)
        if p1 is None or p2 is None:
            return JsonResponse({"Una de las dos personas":"no existe"},status=status.HTTP_400_BAD_REQUEST)
        p1.friends.disconnect(p2)
        return JsonResponse({"relacion":"eliminada"},safe=False)

class followers(APIView):

    def get(self, request, format=None):
        id=request.data['id']
        person = Person.nodes.get(uid=id)
        allfollowers = person.followers
        res = []
        for p in allfollowers:
            res.append({'name':p.name, 'age': p.age, 'id':p.uid})
        return JsonResponse(res,safe=False)