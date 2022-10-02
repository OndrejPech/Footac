import csv
from actions.models import Action

# https://django-extensions.readthedocs.io/en/latest/runscript.html

file_path = ''


def run():
    """
    fill up db with from csv file
    :return:
    """
    with open(file_path) as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # skip headers

        for row in reader:
            side = row[9]
            if not side:  # side is empty string in csv
                side = None
            action, created = Action.objects.get_or_create(type_id=row[4],
                                                           game_id=row[3],
                                                           team_id=row[5],
                                                           opp_team_id=row[6],
                                                           left_pitch_team_id=
                                                           row[7],
                                                           right_pitch_team_id=
                                                           row[8],
                                                           side=side,
                                                           game_time=row[10],
                                                           video_time=row[11])

            if not created:
                print(f'{Action} exists')
                print(row)
