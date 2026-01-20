from django.db import models

# Models for users, teams, activities, leaderboard, and workouts
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(User, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    date = models.DateField()
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    suggested_for = models.ManyToManyField(User, related_name='suggested_workouts', blank=True)

class Leaderboard(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
