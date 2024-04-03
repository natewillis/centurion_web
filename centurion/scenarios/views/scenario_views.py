from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ..models import Scenario

class ScenarioListView(ListView):
    model = Scenario
    template_name = 'scenarios/scenario/scenario_list.html'


class ScenarioDetailView(DetailView):
    model = Scenario
    template_name = 'scenarios/scenario/scenario_detail.html'


class ScenarioCreateView(CreateView):
    model = Scenario
    template_name = 'scenarios/scenario/scenario_form.html'
    fields = ['name', 'exercise_start_datetime']
    success_url = reverse_lazy('scenario_list')

class ScenarioUpdateView(UpdateView):
    model = Scenario
    template_name = 'scenarios/scenario/scenario_form.html'
    fields = ['name', 'exercise_start_datetime']


class ScenarioDeleteView(DeleteView):
    model = Scenario
    template_name = 'scenarios/scenario/scenario_confirm_delete.html'
    success_url = reverse_lazy('scenario_list')
