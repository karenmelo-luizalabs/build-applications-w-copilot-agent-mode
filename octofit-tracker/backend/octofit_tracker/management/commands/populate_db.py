from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            self.stdout.write(self.style.WARNING('Deleting old data...'))
            # Limpar relações ManyToMany antes de deletar qualquer objeto
            for team in Team.objects.all():
                if team.id:
                    team.members.clear()
            for workout in Workout.objects.all():
                if workout.id:
                    workout.suggested_for.clear()
            Activity.objects.all().delete()
            Leaderboard.objects.all().delete()
            Workout.objects.all().delete()
            # Deletar Teams individualmente por id válido
            team_ids = list(Team.objects.values_list('id', flat=True))
            for team_id in team_ids:
                team = Team.objects.filter(id=team_id).first()
                if team and team.id:
                    team.delete()
            # Deletar Users individualmente por id válido
            user_ids = list(User.objects.values_list('id', flat=True))
            for user_id in user_ids:
                user = User.objects.filter(id=user_id).first()
                if user and user.id:
                    user.delete()

            self.stdout.write(self.style.SUCCESS('Creating users...'))
            marvel_heroes = [
                {'username': 'ironman', 'email': 'ironman@marvel.com'},
                {'username': 'captainamerica', 'email': 'cap@marvel.com'},
                {'username': 'spiderman', 'email': 'spiderman@marvel.com'},
            ]
            dc_heroes = [
                {'username': 'batman', 'email': 'batman@dc.com'},
                {'username': 'superman', 'email': 'superman@dc.com'},
                {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com'},
            ]
            marvel_users = [User.objects.create(**hero) for hero in marvel_heroes]
            dc_users = [User.objects.create(**hero) for hero in dc_heroes]

            self.stdout.write(self.style.SUCCESS('Creating teams...'))
            marvel_team = Team.objects.create(name='Marvel')
            marvel_team.members.set(marvel_users)
            dc_team = Team.objects.create(name='DC')
            dc_team.members.set(dc_users)

            self.stdout.write(self.style.SUCCESS('Creating workouts...'))
            workout1 = Workout.objects.create(name='Pushups', description='Do 20 pushups')
            workout2 = Workout.objects.create(name='Running', description='Run 5km')
            workout1.suggested_for.set(marvel_users)
            workout2.suggested_for.set(dc_users)

            self.stdout.write(self.style.SUCCESS('Creating activities...'))
            Activity.objects.create(user=marvel_users[0], activity_type='pushups', duration=10, date='2023-01-01', team=marvel_team)
            Activity.objects.create(user=dc_users[0], activity_type='running', duration=30, date='2023-01-02', team=dc_team)

            self.stdout.write(self.style.SUCCESS('Creating leaderboards...'))
            Leaderboard.objects.create(team=marvel_team, points=100)
            Leaderboard.objects.create(team=dc_team, points=120)

            self.stdout.write(self.style.SUCCESS('Database populated with test data!'))
