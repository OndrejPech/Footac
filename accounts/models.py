from django.db import models
from django.contrib.auth.models import User
from actions.models import Club


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.user)


