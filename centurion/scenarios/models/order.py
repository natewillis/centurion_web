from django.db import models
from datetime import timedelta
from django.templatetags.static import static
from common.utilities.cesium_utilities import CZMLDocument
from .scenario import Scenario 
from ..models.scenario_model import ScenarioModel
import datetime

class Order(ScenarioModel):
    name = models.CharField(max_length=100, default="Unnamed Order")
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='orders')
    offset = models.DurationField(blank=False, null=False, default = timedelta)

    def __str__(self):
        return f'{self.name}'

    def datetime(self):
        return self.scenario.exercise_start_datetime + self.offset
    
    def generate_drone_flight_paths(self):

        # iterate through pickups
        flight_paths = []
        for pickup in self.pickups.all():
            pickup_flight_paths = pickup.generate_drone_flight_paths()
            if len(pickup_flight_paths) > 0:
                flight_paths.extend(pickup_flight_paths)

        return flight_paths

    def generate_visualization_czml(self):

        # create czml document
        czml_document = CZMLDocument(self.datetime(), self.datetime() + datetime.timedelta(hours=2))
        czml_document.add_flight_path_packets(static('common/models/drone.gltf'), self.datetime(), self.generate_drone_flight_paths())

        # return document
        return czml_document