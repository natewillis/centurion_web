from django.db import models

class Scenario(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    exercise_start_datetime = models.DateTimeField(blank=False, null=False)
    
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name