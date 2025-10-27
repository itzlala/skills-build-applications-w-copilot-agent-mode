from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from pymongo import MongoClient

# Sample data for population
def get_sample_data():
    return {
        'users': [
            {'name': 'Superman', 'email': 'superman@dc.com', 'team': 'DC'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'DC'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'DC'},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': 'Marvel'},
            {'name': 'Black Widow', 'email': 'widow@marvel.com', 'team': 'Marvel'},
        ],
        'teams': [
            {'name': 'Marvel'},
            {'name': 'DC'},
        ],
        'activities': [
            {'user': 'superman@dc.com', 'activity': 'Flight', 'duration': 60},
            {'user': 'ironman@marvel.com', 'activity': 'Suit Training', 'duration': 45},
        ],
        'leaderboard': [
            {'user': 'superman@dc.com', 'score': 100},
            {'user': 'ironman@marvel.com', 'score': 95},
        ],
        'workouts': [
            {'name': 'Strength', 'description': 'Heavy lifting'},
            {'name': 'Agility', 'description': 'Speed and movement'},
        ],
    }

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        data = get_sample_data()

        # Clear collections
        for collection in data.keys():
            db[collection].delete_many({})

        # Insert data
        for collection, docs in data.items():
            db[collection].insert_many(docs)

        # Ensure unique index on email for users
        db['users'].create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data!'))
