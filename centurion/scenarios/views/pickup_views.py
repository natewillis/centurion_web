from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ..models import Pickup

class PickupListView(ListView):
    model = Pickup
    template_name = 'pickup_list.html'


class PickupDetailView(DetailView):
    model = Pickup
    template_name = 'pickup_detail.html'


class PickupCreateView(CreateView):
    model = Pickup
    template_name = 'pickup_form.html'
    fields = ['box', 'order', 'offset', 'location', 'altitude_ft']


class PickupUpdateView(UpdateView):
    model = Pickup
    template_name = 'pickup_form.html'
    fields = ['box', 'order', 'offset', 'location', 'altitude_ft']


class PickupDeleteView(DeleteView):
    model = Pickup
    template_name = 'pickup_confirm_delete.html'
    success_url = reverse_lazy('pickup_list')