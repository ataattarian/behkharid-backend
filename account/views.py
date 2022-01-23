from django.shortcuts import render
from .models import User
from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , IsAdminUser ,AllowAny
from rest_framework.views import APIView
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from .serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }





class LoginView(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            user = User.objects.filter(username=data['username'],archive = False).first()
            if not user:
                return Response({
                    'message': _('Username or Password is incorrect')
                },
                    status=status.HTTP_404_NOT_FOUND
                )
            else:
                if user.check_password(serializer.data['password']):
                    return Response({
                        'messages': _('User was authenticated successfully'),
                        'id': user.id,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'token': get_tokens_for_user(user)
                    })
                else:
                    return Response({
                        'messages': _('Username or Password is incorrect')
                    },
                        status=status.HTTP_401_UNAUTHORIZED
                    )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )