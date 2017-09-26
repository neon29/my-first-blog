from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

class User(AbstractUser):
    pass


# triggered as soon as a new user is saved in the db
# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


class Game(models.Model):
    users = models.ManyToManyField(User, through='Membership', related_name='users')
    date_game = models.DateField(default=datetime.date.today)


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, validators=[
            MaxValueValidator(50),
            MinValueValidator(0)
        ])
