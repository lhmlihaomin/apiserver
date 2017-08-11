from django.conf.urls import url
from userapi import views

urlpatterns = [
    url(r'^users/$', views.UserList.as_view(), name='user_list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user_detail'),
    url(r'^token/$', views.gen_token, name='gen_token'),
    url(r'^token/(?P<token>[0-9a-z]+)/$', views.del_token, name='del_token'),
]
