from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from datetime import timedelta
from common.utilities.general_utilities import calculate_hash
from support.utilities import get_elevation
from .pickup import Pickup
from support.models import WorldBorder
from ..models.scenario_model import ScenarioModel


DELIVERY_GENERATE_ATTRIBUTE_VERSION=2

class Delivery(ScenarioModel):
    weight = models.IntegerField(blank=False, null=False, default=0)
    pickup = models.ForeignKey(Pickup, on_delete=models.CASCADE, related_name='deliveries')
    offset = models.DurationField(blank=False, null=False, default=timedelta)
    location = models.PointField(blank=False, null=False, srid=4326, default=Point(-86.6, 34.7))
    altitude_ft = models.FloatField(blank=False, null=False, default=0)
    calculated_altitude_ft = models.FloatField(blank=False, null=False, default=0)
    country = models.ForeignKey('support.WorldBorder', on_delete=models.CASCADE, null=True, blank=True)
    saved_simulated_attribute_hash = models.CharField(max_length=16,blank=True,null=False)
    

    def __str__(self):
        return f'{self.weight} pound delivery'

    def datetime(self):
        return self.pickup.datetime() + self.offset
    
    def simulated_attribute_hash(self):
        return calculate_hash(' '.join([
            f'{DELIVERY_GENERATE_ATTRIBUTE_VERSION}',
            f'{self.offset.total_seconds()}',
            f'{self.location.x:.2f}',
            f'{self.location.y:.2f}',
            ]))

    def generate_attributes(self):

        # calculate country
        print(f'testing to see if {self.location.x} {self.location.y} is in a country')
        self.country = WorldBorder.objects.filter(mpoly__contains=self.location).first()
        print(f'we returned {self.country}')

        # caclulate estimated altitude
        self.calculated_altitude_ft = get_elevation(self.location.y, self.location.x, meters_flag=False)

        # update hash
        self.saved_simulated_attribute_hash = self.simulated_attribute_hash()