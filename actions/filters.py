import django_filters
from .models import Action, Team, Game, Type, Player
from django.db.models import Q


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
        self.filters['type'].label = 'typ'
        self.filters['game'].queryset = Game.objects.filter(Q(home_team_id=self.team_id) | Q(away_team_id=self.team_id))
        self.filters['game'].label = 'zápas'
        self.filters['active_player'].queryset = Player.objects.filter(teams=self.team_id)
        self.filters['active_player'].label = 'hráč'
        self.filters['passive_player'].queryset = Player.objects.filter(teams=self.team_id)
        self.filters['passive_player'].label = 'pas. hráč'

    TEAM_CHOICES = (('attack', 'útočí'), ('defence', 'brání'))  # (value, label)
    PASS_CHOICES = (('no', 'ne'), ('yes', 'ano'))

    team_in_possession = django_filters.ChoiceFilter(label='můj tým', choices=TEAM_CHOICES, method='attack_or_defence')
    # The only one filter with initial value
    show_passes = django_filters.ChoiceFilter(label='zobrazit nahrávky', choices=PASS_CHOICES, method='show_pass', initial='no')

    class Meta:
        model = Action
        fields = ['type', 'game', 'active_player', 'passive_player']

    def attack_or_defence(self, queryset, name,  value):
        if value == 'attack':
            return queryset.filter(team=self.team_id)
        elif value == 'defence':
            return queryset.filter(opp_team=self.team_id)

    def show_pass(self, queryset, name,  value):
        if value == 'no':
            return queryset.exclude(type=2)  # ID 2 belongs to shoot # TODO read file to auto input this id
        else:
            return queryset
