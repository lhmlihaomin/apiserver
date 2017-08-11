import datetime
import pytz

from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework import status

from userapi.models import UserInfo

class ConflictException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Resource already exists."

GENDER_CHOICES = ['female', 'male', 'other']

class UserInfoSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    id = serializers.IntegerField(required=False)
    password = serializers.CharField(max_length=1000, required=False)
    displayName = serializers.CharField(max_length=500, required=False)
    age = serializers.IntegerField(required=False)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=False)


    def create(self, vdata):    # vdata = validated data
        email = vdata.get('email')
        try:
            user = User.objects.get(email=email)
            userinfo = UserInfo.objects.get(user=user)
            #return userinfo
        except User.DoesNotExist:
            # tz = pytz.timezone(settings.TIME_ZONE)
            # now = tz.localize(datetime.datetime.now())
            user = User.objects.create_user(
                username=email.split('@')[0],
                email=email,
                password=vdata.get('password')
            )
            userinfo = UserInfo(
                user=user,
                displayName=vdata.get('displayName'),
                age=vdata.get('age'),
                gender=vdata.get('gender')
            )
            userinfo.save()
            return userinfo
        # raise Exception("User `{0}` already exists.".format(email))
        raise ConflictException(detail="User `{0}` already exists.".format(email))


    def update(self, userinfo, vdata):
        userinfo.displayName = vdata.get('displayName', userinfo.displayName)
        userinfo.age = vdata.get('age', userinfo.age)
        userinfo.gender = vdata.get('gender', userinfo.gender)
        userinfo.save()
        return userinfo
