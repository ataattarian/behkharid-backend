from django.urls import path , include
from rest_framework import routers
from .views import LoginView

router = routers.DefaultRouter()

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]