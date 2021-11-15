from django.urls import path

from redsocial import views

urlpatterns = [
    path('Posts/all/', views.allPosts.as_view()),
    path('Posts/', views.singlePosts.as_view()),
    path('Comments/all/', views.allComments.as_view()),
    path('Persons/', views.singlePerson.as_view()),
    path('Persons/all/', views.allPerson.as_view()),
    path('friends/', views.friends.as_view()),
    path('login/', views.login.as_view()),
]