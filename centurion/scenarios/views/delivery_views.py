from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ..models import Delivery


class DeliveryListView(ListView):
    model = Delivery
    template_name = 'delivery_list.html'


class DeliveryDetailView(DetailView):
    model = Delivery
    template_name = 'delivery_detail.html'


class DeliveryCreateView(CreateView):
    model = Delivery
    template_name = 'delivery_form.html'
    fields = ['weight', 'pickup', 'offset', 'location', 'altitude_ft']


class DeliveryUpdateView(UpdateView):
    model = Delivery
    template_name = 'delivery_form.html'
    fields = ['weight', 'pickup', 'offset', 'location', 'altitude_ft']


class DeliveryDeleteView(DeleteView):
    model = Delivery
    template_name = 'delivery_confirm_delete.html'
    success_url = reverse_lazy('delivery_list')