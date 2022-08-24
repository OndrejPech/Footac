import django_filters
from .models import Action, Team, Game
from django.db.models import Q


class ActionFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        self.team_id = kwargs.pop('team_id')  # new kwarg argument added
        super().__init__(*args, **kwargs)
        # override 'game' filter field, it offers only games where team is included
        self.filters['game'].queryset = Game.objects.filter(Q(home_team_id=self.team_id) | Q(away_team_id=self.team_id))

    class Meta:
        model = Action
        fields = ['type', 'game', 'active_player', 'passive_player']



