from django.db import models
from scenarios.simulation.simulation import simulate_scenario

class ScenarioModel(models.Model):
    class Meta:
        abstract = True

    def save_and_simulate(self, *args, **kwargs):

        # Perform standard save
        self.save(*args, *kwargs)

        # run simulation
        simulate_scenario(self)