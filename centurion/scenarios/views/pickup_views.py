from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from ..models import Pickup, Order
from ..mixins import SaveAndSimulateMixin

class PickupListView(ListView):
    model = Pickup
    template_name = 'scenarios/pickup/pickup_list.html'


class PickupDetailView(DetailView):
    model = Pickup
    template_name = 'scenarios/pickup/pickup_detail.html'


class PickupCreateView(SaveAndSimulateMixin, CreateView):
    model = Pickup
    template_name = 'scenarios/pickup/pickup_form.html'
    fields = ['box', 'order', 'offset', 'location', 'altitude_ft']

    def get_initial(self):
        initial = super().get_initial()
        order_id = self.kwargs.get('order_id')
        if order_id:
            initial['order'] = get_object_or_404(Order, pk=order_id)
        return initial
    
    def get_success_url(self):
        return reverse('pickup_detail', kwargs={'pk': self.object.pk})


class PickupUpdateView(SaveAndSimulateMixin, UpdateView):
    model = Pickup
    template_name = 'scenarios/pickup/pickup_form.html'
    fields = ['box', 'order', 'offset', 'location', 'altitude_ft']

    def get_success_url(self):
        return reverse('pickup_detail', kwargs={'pk': self.object.pk})


class PickupDeleteView(DeleteView):
    model = Pickup
    template_name = 'scenarios/pickup/pickup_confirm_delete.html'
    success_url = reverse_lazy('pickup_list')


def visualize_pickup(request, pk):
    pickup = Pickup.objects.get(pk=pk)
    context = {'pickup': pickup}
    return render(request, 'scenarios/pickup/pickup_visualize.html', context)

def visualize_pickup_czml(request, pk):
    pickup = Pickup.objects.get(pk=pk)
    data = pickup.generate_visualization_czml().to_json()
    return JsonResponse(data, safe=False)