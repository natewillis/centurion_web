from django.test import TestCase
from scenarios.models import Scenario, Order, Pickup, Delivery
from .utilities.general_utilities import get_all_related_objects
from .utilities.astrodynamic_utilities import convert_ECEF_to_geodetic, convert_geodetic_to_ECEF


class GetAllRelatedObjectsTestCase(TestCase):
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


    def test_get_all_related_objects(self):
        related_objects = get_all_related_objects(self.scenario)
        self.assertIn(self.order, related_objects)
        self.assertIn(self.pickup, related_objects)
        self.assertIn(self.delivery, related_objects)
        self.assertNotIn(self.scenario, related_objects)

class ECEFtoGeodeticConversionsTestCase(TestCase):
    def setUp(self):
        self.lon = -93
        self.lat = 43
        self.alt = 0
    
    def test_both(self):
        r1 = convert_geodetic_to_ECEF(self.lat, self.lon, self.alt)
        converted_lat, converted_lon, converted_alt = convert_ECEF_to_geodetic(r1)
        self.assertAlmostEqual(self.lat, converted_lat)
        self.assertAlmostEqual(self.lon, converted_lon)
        self.assertAlmostEqual(self.alt, converted_alt)