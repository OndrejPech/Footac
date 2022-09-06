import csv
from actions.models import Action

# https://django-extensions.readthedocs.io/en/latest/runscript.html

file_path = '/Users/ondrejpech/Desktop/game_01.csv'


def run():
    """
    fill up db with from csv file
    :return:
    """
    with open(file_path) as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # skip headers

        for row in reader:
            # TODO update when final CSV template will be known
            action, created = Action.objects.get_or_create(type_id=row[1],
                                                           game_id=row[2],
                                                           team_id=row[4],
                                                           opp_team_id=row[6],
                                                           game_time=row[9],
                                                           video_time=row[10])

            if created:
                print(f'{Action} exists')
