from math import radians, sin, cos, sqrt, atan2, degrees
from django.contrib.gis.geos import Point

def great_circle_distance(point1, point2):
    """
    Calculate the great circle distance in nautical miles between two points.

    Args:
    point1 (GEOSGeometry): First point in SRID 4326.
    point2 (GEOSGeometry): Second point in SRID 4326.

    Returns:
    float: Great circle distance in nautical miles.
    """
    # Earth's radius in nautical miles
    R = 3440.065

    # Convert latitude and longitude from degrees to radians
    lat1 = radians(point1.y)
    lon1 = radians(point1.x)
    lat2 = radians(point2.y)
    lon2 = radians(point2.x)

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


def intermediate_point(point1, point2, fraction):
    """
    Calculate an intermediate point along a great circle path between two points.

    Args:
    point1 (GEOSGeometry): First point in SRID 4326.
    point2 (GEOSGeometry): Second point in SRID 4326.
    fraction (float): Fraction along the great circle route (0 is point1, 1 is point2).

    Returns:
    GEOSGeometry: Intermediate point in SRID 4326.
    """
    # Convert latitude and longitude from degrees to radians
    lat1 = radians(point1.y)
    lon1 = radians(point1.x)
    lat2 = radians(point2.y)
    lon2 = radians(point2.x)
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Angular distance between the points
    delta = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    delta = 2 * atan2(sqrt(delta), sqrt(1 - delta))

    # Intermediate point calculations
    a = sin((1 - fraction) * delta) / sin(delta)
    b = sin(fraction * delta) / sin(delta)
    x = a * cos(lat1) * cos(lon1) + b * cos(lat2) * cos(lon2)
    y = a * cos(lat1) * sin(lon1) + b * cos(lat2) * sin(lon2)
    z = a * sin(lat1) + b * sin(lat2)
    lat_i = degrees(atan2(z, sqrt(x**2 + y**2)))
    lon_i = degrees(atan2(y, x))

    # Convert back to degrees and create a GEOSGeometry object
    intermediate_point = Point(x=lon_i, y=lat_i, srid=4326)
    print(f'intermediate point is {intermediate_point}')
    return intermediate_point