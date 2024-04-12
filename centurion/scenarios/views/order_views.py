from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from ..models import Order, Scenario


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

    def get_initial(self):
        initial = super().get_initial()
        scenario_id = self.kwargs.get('scenario_id')
        if scenario_id:
            initial['scenario'] = get_object_or_404(Scenario, pk=scenario_id)
        return initial


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'scenarios/order/order_form.html'
    fields = ['name', 'scenario', 'offset']


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'scenarios/order/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')

def visualize_order(request, pk):
    order = Order.objects.get(pk=pk)
    context = {'order': order}
    return render(request, 'scenarios/order/order_visualize.html', context)

def visualize_order_czml(request, pk):
    order = Order.objects.get(pk=pk)
    data = order.generate_visualization_czml().to_json()
    return JsonResponse(data, safe=False)