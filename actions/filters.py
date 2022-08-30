import django_filters
from .models import Action, Team, Game, Type, Player
from django.db.models import Q


class ActionFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        self.team_id = kwargs.pop('team_id')  # new kwarg argument added
        super().__init__(*args, **kwargs)
        # override fields
        self.filters['type'].label = 'typ'
        self.filters['game'].queryset = Game.objects.filter(Q(home_team_id=self.team_id) | Q(away_team_id=self.team_id))
        self.filters['game'].label = 'zápas'
        self.filters['active_player'].queryset = Player.objects.filter(teams=self.team_id)
        self.filters['active_player'].label = 'hráč'
        self.filters['passive_player'].queryset = Player.objects.filter(teams=self.team_id)
        self.filters['passive_player'].label = 'pas. hráč'

    CHOICES = (
        ('attack', 'útočí'), ('defence', 'brání')
    )

    team_in_possession = django_filters.ChoiceFilter(label='můj tým', choices=CHOICES, method='attack_or_defence')

    class Meta:
        model = Action
        fields = ['type', 'game', 'active_player', 'passive_player']

    def attack_or_defence(self, queryset, name,  value):
        if value == 'attack':
            return queryset.filter(team=self.team_id)
        elif value == 'defence':
            return queryset.filter(opp_team=self.team_id)
