from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from datetime import timedelta
from .pickup import Pickup

class Delivery(models.Model):
    weight = models.IntegerField(blank=False, null=False, default=0)
    pickup = models.ForeignKey(Pickup, on_delete=models.CASCADE, related_name='deliveries')
    offset = models.DurationField(blank=False, null=False, default=timedelta)
    location = models.PointField(blank=False, null=False, srid=4326, default=Point(-86.6, 34.7))
    altitude_ft = models.FloatField(blank=False, null=False, default=0)
    saved_simulated_attribute_hash = models.CharField(max_length=16,blank=True,null=False)

    def __str__(self):
        return f'{self.weight} pound delivery'

    def datetime(self):
        return self.pickup.datetime() + self.offset
    