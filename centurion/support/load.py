from .models import Elevation
from django.contrib.gis.gdal import GDALRaster


def import_elevation_data():

    # import raster
    elevation_raster = GDALRaster("data\\reprojected_downsampled_ETOPO.tif", write=True)
    print("Raster object created successfully.")
    print(f"Raster size: {elevation_raster.width}x{elevation_raster.height}")
    print(f"Number of bands: {elevation_raster.bands}")
    print(f"SRID: {elevation_raster.srs.srid if elevation_raster.srs else 'None'}")

    # Create elevation object
    new_elevation_object = Elevation.objects.create(raster=elevation_raster,name="ETOPO 2022")
    new_elevation_object.save()