from django.test import TestCase
from django.urls import reverse
from scenarios.models import Scenario, Order, Pickup, Delivery
from support.models import WorldBorder
from support.load import import_world_border_data
from .simulation.simulation import simulate_scenario


class SimulationTestCase(TestCase):
    def setUp(self):
        
        # create scenario
        self.scenario = Scenario.objects.create()
        self.scenario.save()

        # create order
        self.order = Order.objects.create(scenario=self.scenario)
        self.order.save()

        # create pickup
        self.pickup = Pickup.objects.create(order=self.order)
        self.pickup.save()

        # create delivery
        self.delivery = Delivery.objects.create(pickup=self.pickup)
        self.delivery.save()

        # load worldborders
        import_world_border_data()
        self.us = WorldBorder.objects.get(fips="US")


    def test_simulation(self):
        simulate_scenario(self.scenario)
        self.pickup.refresh_from_db()
        self.assertEqual(self.pickup.country, self.us)
        self.delivery.refresh_from_db()
        self.assertEqual(self.delivery.country, self.us)


class SaveAndSimulateMixinTestCase(TestCase):
    def setUp(self):
        
        # create scenario
        self.scenario = Scenario.objects.create()
        self.scenario.save()

        # create order
        self.order = Order.objects.create(scenario=self.scenario)
        self.order.save()

        # create pickup
        self.pickup = Pickup.objects.create(order=self.order)
        self.pickup.save()

        # create delivery
        self.delivery = Delivery.objects.create(pickup=self.pickup)
        self.delivery.save()

        # load worldborders
        import_world_border_data()
        self.us = WorldBorder.objects.get(fips="US")


    def test_simulation(self):
        
        # URL mapping that needs to be configured in urls.py for the view
        url = reverse('delivery_create')  
        response = self.client.post(url, {'pickup': self.pickup.id})

        # Check response status code
        self.assertEqual(response.status_code, 302)  # Redirect to success_url

        # Check if the object was created and simulated correctly
        simulated_delivery = Delivery.objects.last()
        self.assertIsNotNone(simulated_delivery)
        self.assertEqual(simulated_delivery.id, 2)
        self.assertEqual(simulated_delivery.country, self.us)
        