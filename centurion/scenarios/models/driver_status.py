from django.db import models
from datetime import timedelta
from .scenario import Scenario 
from ..models.scenario_model import ScenarioModel


class DriverStatus(ScenarioModel):

    STATUS_CHOICES = (
        ('GD', 'GOOD TO GO'),
        ('TD', 'TIRED'),
        ('IN', 'INJURED')
    )

    name = models.CharField(max_length=100, default="Unnamed Order")
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='orders')
    offset = models.DurationField(blank=False, null=False, default = timedelta)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='GD')

    def __str__(self):
        return f'{self.name} is {self.status}'

    def datetime(self):
        return self.scenario.exercise_start_datetime + self.offset