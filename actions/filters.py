import django_filters
from .models import Action, Team, Game, Type, Player
from django.db.models import Q
from .db_data import LEFT_SIDE_ID, RIGHT_SIDE_ID, ACTIONS_IDS


class ActionFilter(django_filters.FilterSet):

    def __init__(self, data=None, *args, **kwargs):

        # if filterset is bound, use initial values as defaults
        if data is not None:
            data = data.copy()  # get a mutable copy of the QueryDict
            for name, filter_object in self.base_filters.items():
                initial = filter_object.extra.get('initial')
                # filter param is either missing or empty, use initial as default
                if not data.get(name) and initial:
                    data[name] = initial

        self.team_id = kwargs.pop('team_id')  # new kwarg argument added
        super().__init__(data, *args, **kwargs)
        # override fields
        self.filters['type'].label = 'typ akce'
        self.filters['game'].queryset = Game.objects.filter(
            Q(home_team_id=self.team_id) | Q(away_team_id=self.team_id))
        self.filters['game'].label = 'zápas'
        self.filters['active_player'].queryset = Player.objects.filter(
            teams=self.team_id)
        self.filters['active_player'].label = 'hráč'
        self.filters['passive_player'].queryset = Player.objects.filter(
            teams=self.team_id)
        self.filters['passive_player'].label = 'pas. hráč'

    TEAM_CHOICES = (('attack', 'útočí'), ('defence', 'brání'))  # (value, label)
    PASS_CHOICES = (('no', 'ne'), ('yes', 'ano'))
    FIELD_CHOICES = (('attacking', 'útočná'), ('defending', 'obranná'),
                     ('no_data', 'neznámá'))

    team_in_possession = django_filters.ChoiceFilter(label='můj tým',
                                                     choices=TEAM_CHOICES,
                                                     method='attack_or_defence')
    field_half = django_filters.ChoiceFilter(label='polovina hřiště',
                                             choices=FIELD_CHOICES,
                                             method='show_field_half')
    # The only one filter with initial value
    show_passes = django_filters.ChoiceFilter(label='zobrazit nahrávky',
                                              choices=PASS_CHOICES,
                                              method='show_pass', initial='no')

    class Meta:
        model = Action
        fields = ['type', 'game', 'team_in_possession', 'field_half',
                  'active_player', 'passive_player']

    def attack_or_defence(self, queryset, name, value):
        if value == 'attack':
            return queryset.filter(team=self.team_id)
        elif value == 'defence':
            return queryset.filter(opp_team=self.team_id)

    def show_pass(self, queryset, name, value):
        if value == 'no':
            return queryset.exclude(
                type__in=[ACTIONS_IDS['pass'], ACTIONS_IDS['lob']])
        else:
            return queryset

    def show_field_half(self, queryset, name, value):
        if value == 'attacking':
            return queryset.filter(
                Q(left_pitch_team=self.team_id, side=RIGHT_SIDE_ID) | Q(
                    right_pitch_team=self.team_id, side=LEFT_SIDE_ID))
        elif value == 'defending':
            return queryset.filter(
                Q(left_pitch_team=self.team_id, side=LEFT_SIDE_ID) | Q(
                    right_pitch_team=self.team_id, side=RIGHT_SIDE_ID))
        elif value == 'no_data':
            return queryset.filter(side=None)
