from django.contrib.gis.db import models
from .scenario import Scenario 

class Order(models.Model):
    name = models.CharField(max_length=100)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='orders')
    offset = models.DurationField(blank=False, null=False)

    def __str__(self):
        return f'{self.name}'

    def datetime(self):
        return self.scenario.exercise_start_datetime + self.offset