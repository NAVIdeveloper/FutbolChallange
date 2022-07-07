from django import template
from ..models import *
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Max,Min,Q as SearchQ
# .aggregate(Max('intended_weight'))['intended_weight__max'])

register = template.Library()

@register.filter(name='index')
def find_index(a, l):
    l = list(l.order_by('-PTS'))
    return l.index(a)+1


@register.filter(name='pts')
def index_pts(a):
    l = a.order_by('-PTS')
    return l

@register.filter(name="get_teams")
def get_teams(a):
    teams = serializers.serialize('json', RegisterTeam.objects.filter(turnament=a))
    
    return JsonResponse(teams)

@register.filter(name='round_index')
def index_round(l):
    rounds = l.aggregate(Max('round'))['round__max']
    return range(1,rounds+1)
