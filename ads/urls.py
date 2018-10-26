from django.urls import path

from . import views

app_name = 'ads'

urlpatterns = [
    path('<int:pk>/', views.AdClickView.as_view(), name='ad-click'),
    path('random-ad/<str:zone>/<str:group>/',
         views.random_ad, name='random-ad'),
    path('static-ad/<str:title>/<str:zone>/',
         views.static_ad, name='static-ad'),
]
