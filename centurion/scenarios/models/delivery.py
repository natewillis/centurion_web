from django.db import models
from .pickup import Pickup

class Delivery(models.Model):
    weight = models.IntegerField(blank=False, null=False)
    pickup = models.ForeignKey(Pickup, on_delete=models.CASCADE, related_name='deliveries')
    offset = models.DurationField(blank=False, null=False)
    #location = models.PointField(blank=False, null=False, srid=4326)
    altitude_ft = models.FloatField(blank=False, null=False)

    def __str__(self):
        return f'{self.weight} pound delivery'

    def datetime(self):
        return self.pickup.datetime() + self.offset
    