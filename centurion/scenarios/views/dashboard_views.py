from django.shortcuts import render
from ..models import Scenario

def scenario_dashboard(request, pk):
    scenario = Scenario.objects.get(pk=pk)
    context = {'scenario': scenario}
    return render(request, 'scenarios/dashboards/scenario_dashboard.html', context)