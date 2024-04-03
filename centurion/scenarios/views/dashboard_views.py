from django.shortcuts import render
from ..models import Scenario, Order

def scenario_dashboard(request, pk):
    scenario = Scenario.objects.get(pk=pk)
    context = {'scenario': scenario}
    return render(request, 'scenarios/dashboards/scenario_dashboard.html', context)

def order_dashboard(request, pk):
    order = Order.objects.get(pk=pk)
    context = {'order': order}
    return render(request, 'scenarios/dashboards/order_dashboard.html', context)