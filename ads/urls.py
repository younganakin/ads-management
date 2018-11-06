from django.urls import path

from . import views

app_name = 'ads'

urlpatterns = [
    path('<int:pk>/', views.AdClickView.as_view(), name='ad-click'),
]
