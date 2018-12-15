from django_extensions.management.jobs import DailyJob
import requests

# 1. Activate virtual env -> conda.  2. The command line |
# source activate /anaconda3/envs/IS590WFO_final_project
# python manage.py runjob renew_grid_player_data


class Job(DailyJob):
    help = """Daily job that sends a GET request to the Django server 
    for the url path of 'daily_update/' to update the database daily"""

    URL = "http://127.0.0.1:8000/daily_update/"  # Hard coded at the moment <-- Needs change when deployed on the web!

    def execute(self):
        # send GET request to the url
        r = requests.get(url=self.URL)
        print(r)
