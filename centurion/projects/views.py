from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Project
from .forms import ProjectForm


class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/project_list.html'


class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/project_list.html'


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')
