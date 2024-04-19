from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.templatetags.static import static
from datetime import timedelta
from .order import Order
from common.utilities.general_utilities import calculate_hash
from common.utilities.astrodynamic_utilities import generate_drone_path, generate_drone_seperation_point_and_timedelta
from common.utilities.cesium_utilities import Packet, CZMLDocument
from support.utilities import get_elevation
from support.models import Box, WorldBorder
from ..models.scenario_model import ScenarioModel
import datetime

PICKUP_GENERATE_ATTRIBUTE_VERSION=2
FEET_PER_NAUTICAL_MILE = 6076

class Pickup(ScenarioModel):
    box = models.ForeignKey(Box, on_delete=models.CASCADE, default=Box.get_default_pk)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='pickups')
    offset = models.DurationField(blank=False, null=False, default=timedelta)
    location = models.PointField(blank=False, null=False, srid=4326, default=Point(-95.9, 41.2))
    altitude_ft = models.FloatField(blank=False, null=False, default=0)
    calculated_altitude_ft = models.FloatField(blank=False, null=False, default=0)
    country = models.ForeignKey('support.WorldBorder', on_delete=models.CASCADE, null=True, blank=True)
    saved_simulated_attribute_hash = models.CharField(max_length=16,blank=True,null=False)

    def __str__(self):
        return f'{self.box.name} pickup'

    def datetime(self):
        return self.order.datetime() + self.offset
    

    def simulated_attribute_hash(self):
        return calculate_hash(' '.join([
            f'{PICKUP_GENERATE_ATTRIBUTE_VERSION}',
            f'{self.offset.total_seconds()}',
            f'{self.location.x:.2f}',
            f'{self.location.y:.2f}',
            ]))

    def generate_attributes(self):

        # calculate country
        self.country = WorldBorder.objects.filter(mpoly__contains=self.location).first()

        # caclulate estimated altitude
        self.calculated_altitude_ft = get_elevation(self.location.y, self.location.x, meters_flag=False)

        # calculate drone path

        # update hash
        self.saved_simulated_attribute_hash = self.simulated_attribute_hash()


    def key_impact(self):
        try:
            return self.deliveries.earliest('id')
        except Pickup.DoesNotExist:
            return None
        
    def generate_drone_flight_paths(self):

        # create end_point lists
        end_points = []
        end_timedeltas = []
        end_altitudes = []
        for delivery in self.deliveries.order_by('id'):
            end_points.append(delivery.location)
            end_timedeltas.append(delivery.offset)
            end_altitudes.append(delivery.altitude_ft/FEET_PER_NAUTICAL_MILE)
        
        # get flight paths
        print(f'flight path location is {self.location}')
        flight_paths = generate_drone_path(self.location, self.altitude_ft/FEET_PER_NAUTICAL_MILE, end_points, end_altitudes, end_timedeltas)

        return flight_paths

    def generate_visualization_czml(self):

        # create czml document
        czml_document = CZMLDocument(self.datetime(), self.datetime() + datetime.timedelta(hours=2))
        czml_document.add_flight_path_packets(static('common/models/drone.gltf'), self.datetime(), self.generate_drone_flight_paths())

        # return document
        return czml_document