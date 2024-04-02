from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ..models import Order


class OrderListView(ListView):
    model = Order
    template_name = 'scenarios/order/order_list.html'


class OrderDetailView(DetailView):
    model = Order
    template_name = 'scenarios/order/order_detail.html'


class OrderCreateView(CreateView):
    model = Order
    template_name = 'scenarios/order/order_form.html'
    fields = ['name', 'scenario', 'offset']
    success_url = reverse_lazy('order_list')


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'scenarios/order/order_form.html'
    fields = ['name', 'scenario', 'offset']


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'scenarios/order/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')