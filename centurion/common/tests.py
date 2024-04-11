from django.test import TestCase
from scenarios.models import Scenario, Order, Pickup, Delivery
from django.contrib.gis.geos import GEOSGeometry
from .utilities.general_utilities import get_all_related_objects
from .utilities.astrodynamic_utilities import convert_ECEF_to_geodetic, convert_geodetic_to_ECEF, greenwich_sidereal_time
from .utilities.geospatial_utilities import great_circle_distance, intermediate_point
import datetime

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
    
    def test_convert_geodetic_to_ECEF(self):
        r1 = convert_geodetic_to_ECEF(self.lat, self.lon, self.alt)
        print(f'r1 is {r1 }')
        self.assertAlmostEqual(r1[0], -131.27138439572073, 0)
        self.assertAlmostEqual(r1[1], -2519.196, 0)
        self.assertAlmostEqual(r1[2], 2336.6641469, 0)

    def test_convert_ECEF_to_geodetic(self):
        converted_lat, converted_lon, converted_alt = convert_ECEF_to_geodetic([-132.025378, -2519.196, 2336.661469])
        print(f'return is is {converted_lat}, {converted_lon}, {converted_alt}')
        self.assertAlmostEqual(self.lat, converted_lat , 0)
        self.assertAlmostEqual(self.lon, converted_lon, 0)
        self.assertAlmostEqual(self.alt, converted_alt, 0)

    def test_both(self):
        r1 = convert_geodetic_to_ECEF(self.lat, self.lon, self.alt)
        converted_lat, converted_lon, converted_alt = convert_ECEF_to_geodetic(r1)
        self.assertAlmostEqual(self.lat, converted_lat, 0)
        self.assertAlmostEqual(self.lon, converted_lon, 0)
        self.assertAlmostEqual(self.alt, converted_alt, 0)

class GreenwichSiderealTimeTestCase(TestCase):
    def test_greenwich_sidereal_time(self):
        time_to_convert = datetime.datetime(year=2004, month=3, day=3, hour=4, minute=30)
        converted_time = greenwich_sidereal_time(time_to_convert)
        self.assertAlmostEqual(converted_time, 228.79354,3)

class GreatCircleDistanceTestCase(TestCase):
    def test_great_circle_distance(self):
        point1 = GEOSGeometry('POINT(-73.985656 40.748433)', srid=4326)  # Empire State Building
        point2 = GEOSGeometry('POINT(-74.044500 40.689247)', srid=4326)  # Statue of Liberty
        great_circle_distance_return = great_circle_distance(point1, point2)  # Distance in nautical miles
        self.assertAlmostEqual(great_circle_distance_return, 4.45, 3)

class IntermediatePointTestCase(TestCase):
    def test_intermediate_point(self):
        point1 = GEOSGeometry('POINT(-5 50)', srid=4326)  # Empire State Building
        point2 = GEOSGeometry('POINT(-3 58)', srid=4326)  # Statue of Liberty
        return_point = intermediate_point(point1, point2, 0.5)  # Distance in nautical miles
        self.assertAlmostEqual(return_point.x, -4.09638889, 3)
        self.assertAlmostEqual(return_point.y, 54.00416667, 3)