

from django.db import models
from bson import ObjectId

def generate_objectid():
    return str(ObjectId())

# Models for users, teams, activities, leaderboard, and workouts
class User(models.Model):
    id = models.CharField(primary_key=True, max_length=24, default=generate_objectid, editable=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class Team(models.Model):
    id = models.CharField(primary_key=True, max_length=24, default=generate_objectid, editable=False)
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(User, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)

class Activity(models.Model):
    id = models.CharField(primary_key=True, max_length=24, default=generate_objectid, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    date = models.DateField()
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

class Workout(models.Model):
    id = models.CharField(primary_key=True, max_length=24, default=generate_objectid, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    suggested_for = models.ManyToManyField(User, related_name='suggested_workouts', blank=True)

class Leaderboard(models.Model):
    id = models.CharField(primary_key=True, max_length=24, default=generate_objectid, editable=False)
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
