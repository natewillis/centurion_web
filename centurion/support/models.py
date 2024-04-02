from django.contrib.gis.db import models


#class Elevation(models.Model):
#    name = models.CharField(max_length=100)
#    raster = models.RasterField()


class Box(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
