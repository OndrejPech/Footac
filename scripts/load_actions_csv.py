import csv
from actions.models import Action

# https://django-extensions.readthedocs.io/en/latest/runscript.html

file_path = '/Users/ondrejpech/Desktop/backup matches/zruc-sla 1 half.csv'


def run():
    """
    fill up db with from csv file
    :return:
    """
    with open(file_path) as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # skip headers

        for row in reader:
            action, created = Action.objects.get_or_create(type_id=row[4],
                                                           game_id=row[3],
                                                           team_id=row[5],
                                                           opp_team_id=row[6],
                                                           left_pitch_team_id=row[7],
                                                           right_pitch_team_id=row[8],
                                                           game_time=row[9],
                                                           video_time=row[10])

            if not created:
                print(f'{Action} exists')
                print(row)
