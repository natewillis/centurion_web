from django.contrib.gis.db import models
from .order import Order

class Pickup(models.Model):
    box = models.ForeignKey("support.Box", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='pickups')
    offset = models.DurationField(blank=False, null=False)
    location = models.PointField(blank=False, null=False, srid=4326)
    altitude_ft = models.FloatField(blank=False, null=False)

    def __str__(self):
        return f'{self.box} pickup'

    def datetime(self):
        return self.order.datetime + self.offset