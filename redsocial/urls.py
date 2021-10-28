from django.urls import path

from redsocial import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Posts/all', views.allPosts.as_view()),
    path('Posts/', views.singlePosts.as_view()),
    path('Cities', views.allCities.as_view()),
    path('Post/crear', views.hacerPost),
    path('Persons/', views.singlePerson.as_view()),
    path('Persons/all', views.allPerson.as_view()),
]