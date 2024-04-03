from django.db import models


#class Elevation(models.Model):
#    name = models.CharField(max_length=100)
#    raster = models.RasterField()


class Box(models.Model):
    name = models.CharField(max_length=100)

    @classmethod
    def get_default_pk(cls):
        box, created = cls.objects.get_or_create(
            name='standard box', 
        )
        return box.pk

    def __str__(self):
        return self.name
