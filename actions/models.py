from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Club(models.Model):
    name = models.CharField(max_length=128)
    abbrev = models.CharField(max_length=16)
    email = models.EmailField(null=True, blank=True, )
    address = models.CharField(max_length=256, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True,
                             upload_to="static/img/logos")

    def __str__(self):
        return self.name


class Squad(models.Model):
    name = models.CharField(max_length=32)  # like  A, B ,Woman, U18

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Team(models.Model):
    squad = models.ForeignKey(Squad, default=1, on_delete=models.CASCADE,
                              related_name='squad_teams')
    abbrev = models.CharField(max_length=16)
    club = models.ForeignKey(Club, on_delete=models.CASCADE,
                             related_name='teams')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.club.name} {self.squad}'


class League(models.Model):
    name = models.CharField(max_length=128)
    abbrev = models.CharField(null=True, max_length=16)

    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Game(models.Model):
    date = models.DateField()
    home_team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL,
                                  related_name='home_games')
    away_team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL,
                                  related_name='away_games')
    home_score = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(99)])
    away_score = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(99)])
    penalty_dec = models.BooleanField(default=False)
    extra_time_dec = models.BooleanField(default=False)
    no_winner = models.BooleanField(default=False)
    home_team_possession = models.IntegerField(null=True, blank=True,
                                               validators=[MinValueValidator(1),
                                                           MaxValueValidator(
                                                               99)])
    away_team_possession = models.IntegerField(null=True, blank=True,
                                               validators=[MinValueValidator(1),
                                                           MaxValueValidator(
                                                               99)])
    team_won = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL,
                                 related_name='won_games')
    team_lose = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL,
                                  related_name='lose_games')
    season = models.ForeignKey(Season, null=True, on_delete=models.SET_NULL,
                               related_name='season_games')
    league = models.ForeignKey(League, null=True, on_delete=models.SET_NULL,
                               related_name='league_games')
    recorded = models.BooleanField(default=False)
    link_1 = models.URLField(null=True, blank=True)
    link_2 = models.URLField(null=True, blank=True)
    link_3 = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.date}, {self.home_team} {self.home_score}:{self.away_score} {self.away_team}'


class Person(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, db_collation='cs_CZ.UTF-8')
    birth_day = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True  # this class will not be DB table, works only as parent class


class Player(Person):
    club = models.ForeignKey(Club, null=True, on_delete=models.SET_NULL,
                             related_name='players')
    teams = models.ManyToManyField(Team, blank=True, related_name='players')

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Type(models.Model):
    name = models.CharField(max_length=64)
    name_cz = models.CharField(max_length=64)

    class Meta:
        ordering = ['name_cz']

    def __str__(self):
        return self.name_cz


class Subtype(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE,
                             related_name='subtypes')
    name = models.CharField(max_length=64)
    name_cz = models.CharField(max_length=64)

    def __str__(self):
        return self.name_cz


class Action(models.Model):
    class Side(models.IntegerChoices):
        LEFT = 1
        RIGHT = 2

    type = models.ForeignKey(Type, null=True, on_delete=models.SET_NULL,
                             related_name='type_actions')
    subtype = models.ForeignKey(Subtype, null=True, on_delete=models.SET_NULL,
                                related_name='subtype_actions')
    game = models.ForeignKey(Game, on_delete=models.CASCADE,
                             related_name='game_actions')
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL,
                             related_name='team_actions')
    opp_team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL,
                                 related_name='opp_team_actions')
    active_player = models.ForeignKey(Player, null=True, blank=True,
                                      on_delete=models.SET_NULL,
                                      related_name='active_player_actions')
    passive_player = models.ForeignKey(Player, null=True, blank=True,
                                       on_delete=models.SET_NULL,
                                       related_name='passive_player_actions')
    game_time = models.IntegerField(validators=[MinValueValidator(0),
                                                MaxValueValidator(
                                                    10000)])  # in seconds
    video_time = models.IntegerField(validators=[MinValueValidator(0),
                                                 MaxValueValidator(
                                                     10000)])  # in seconds
    left_pitch_team = models.ForeignKey(Team, null=True,
                                        on_delete=models.SET_NULL,
                                        related_name='left_pitch_teams')
    right_pitch_team = models.ForeignKey(Team, null=True,
                                         on_delete=models.SET_NULL,
                                         related_name='right_pitch_teams')
    side = models.IntegerField(choices=Side.choices, null=True, blank=True)
    start_x = models.IntegerField(null=True, blank=True)
    start_y = models.IntegerField(null=True, blank=True)
    end_x = models.IntegerField(null=True, blank=True)
    end_y = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-game', 'game_time']

    def display_time(self):
        m, s = divmod(self.game_time, 60)
        return f'{m:02d}:{s:02d}'

    def __str__(self):
        # if I use self.display_time, program goes to infinitive recrusion loop,
        # so I need to calculate it here
        m, s = divmod(self.game_time, 60)
        time = f'{m:02d}:{s:02d}'
        return f'{time} {self.type.name} vs. {self.opp_team}'
