from math import atan2, asin, acos, sin, cos, sqrt


RADIUS_EARTH_NM = 3443.92
DEGREES_TO_RADIANS = .01745
E2 = 0.00669437999014

# From Converting between ECEF and Geodetic coordinates, D. Rose - November 2014
def convert_ECEF_to_geodetic(r1):

    a = RADIUS_EARTH_NM
    
    a1 = 23.0549091356429
    a2 = 531.528835252753
    a3 = 0.077169161196072
    a4 = 1328.82208813188
    a5 = 23.132078296839
    a6 = 0.99330562000986

    # do the conversion
    x = r1[0]
    y = r1[1]
    z = r1[2]

    zp = abs(z)
    w2 = x*x + y*y
    w = sqrt(w2)
    r2 = w2 + z*z
    r = sqrt(r2)
    lon = atan2(y, x)

    s2 = z * z / r2
    c2 = w2 / r2
    u = a2 / r
    v = a3 - a4 / r

    if c2 > 0.3:
        s = (zp / r) * (1 + c2 * (a1 + u + s2 * v) / r)
        lat = asin(s)
        ss = s ** s
        c = sqrt(1 - ss)
    else:
        c = (w / r) * (1  - s2 * (a5 - u - c2 * v) / r)
        lat = acos(c)
        ss = 1 - c * c
        s = sqrt(ss)

    g = 1 - E2 * ss
    rg = a / sqrt( g)
    rf = a6 * rg
    u = w - rg * c
    v = zp - rf * s
    f = c * u + s * v
    m = c * v - s * u
    p = m / (rf / g + f)
    lat = lat + p
    alt = f + m * p / 2
    if z < 0:
        lat = lat * -1
    
    return lat/DEGREES_TO_RADIANS, lon/DEGREES_TO_RADIANS, alt


# From Converting between ECEF and Geodetic coordinates, D. Rose - November 2014
def convert_geodetic_to_ECEF(lat_degrees, lon_degrees, alt_nm):

    # conversions
    lat = lat_degrees  * DEGREES_TO_RADIANS
    lon = lon_degrees * DEGREES_TO_RADIANS

    # ijk calcs
    cos_lat = cos(lat)
    sin_lat = sin(lat)
    n = RADIUS_EARTH_NM / sqrt(1 - E2 * sin_lat * sin_lat)
    iprime = (n + alt_nm) * cos_lat * cos(lon)
    jprime = (n + alt_nm) * cos_lat * sin(lon)
    kprime = (n * (1 - E2) + alt_nm) * sin_lat

    # return
    return [iprime, jprime, kprime]