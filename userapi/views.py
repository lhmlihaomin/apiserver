# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from userapi.models import UserInfo
from userapi.serializers import UserInfoSerializer
from userapi.permissions import IsOwner

class UserList(generics.CreateAPIView):
    """
    List users or create a new user.
    """
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

class UserDetail(generics.RetrieveUpdateAPIView):
    """
    Display user detail or update user info.
    """
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwner)

@api_view(['POST'])
def gen_token(request):
    """
    Authenticate user and return one's token.
    A token is created if user doesn't have one.
    """
    try:
        user = User.objects.get(email=request.data.get('email'))
    except User.DoesNotExist:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    password = request.data.get('password')
    if not user.check_password(password):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        token = Token.objects.create(user=user)
    return Response(data={
        'id': user.id,
        'token': token.key
    })


@api_view(['DELETE'])
def del_token(request, token):
    """
    Delete the requested token.
    """
    if request.user.is_anonymous():
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        token = Token.objects.get(user=request.user)
    except Token.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    token.delete()
    return Response("yahaha!")
