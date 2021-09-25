from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('home', views.index),
    path('about', views.about),
    path('location', views.location),
    path('events', views.events),
    path('gallery', views.gallery),
    path('register', views.register),
    path('login', views.login),
    path('register_action', views.register_action),
    path('login_action', views.login_action),
    path('logout', views.logout),
    path('posts', views.posts),
    path('view_user/<int:userid>', views.view_user),
    path('update', views.update),
    path('update/<int:userid>', views.update),
    path('process_update/<int:userid>', views.process_update),
    path('addlike/<int:post_id>', views.addlike),
    path('addpost', views.addpost),
    path('delete/<int:post_id>', views.delete)
]
