from collections import defaultdict
from common.utilities.general_utilities import get_all_related_objects

def simulate_scenario(scenario):
    
    # TODO: gather data from cache
    # TODO: summarize orders so we can directly put data in the dashboard without queries
    # Gather data
    
    # Get all related objects
    related_objects = get_all_related_objects(scenario)

    # create timed hash
    objects_by_time = sorted(related_objects, key=lambda x: x.datetime())

    # iterate objects
    for object in objects_by_time:
        print(object)