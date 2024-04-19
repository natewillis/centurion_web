from django.db import connection

def get_elevation(lat, lon, meters_flag):
    # Convert the latitude and longitude to a Point geometry
    point_string = f'ST_SetSRID(ST_MakePoint({lon}, {lat}), 4326)'

    # Construct the SQL query to extract the elevation value
    sql = f'''
        SELECT ST_Value(raster, {point_string})
        FROM support_elevation
        WHERE ST_Intersects(raster, {point_string});
    '''

    # Execute the query
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchone()

    # Return the elevation value as a JSON response
    if result:
        if not meters_flag:
            elevation = result[0] * 3.281
        else:
            elevation = result[0]
        return elevation
    else:
        return 0