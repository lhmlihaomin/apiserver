# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    """
    Additional user info
    """
    user = models.ForeignKey(User)
    displayName = models.CharField(max_length=500, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)

    @property
    def email(self):
        return self.user.email
