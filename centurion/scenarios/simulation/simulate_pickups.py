import logging
from .utilities import add_instance_to_changed_types

# create logger
logger = logging.getLogger(__name__)

def simulate_pickups(pickups, simulation_data):
    
    # generate attributes
    for pickup in pickups:

        # simulated attributes
        if pickup.simulated_attribute_hash() != pickup.saved_simulated_attribute_hash:
            logger.debug(f'pickups: before generate country is {pickup.country}')
            pickup.generate_attributes()
            logger.debug(f'pickups: after generate country is {pickup.country}')
            add_instance_to_changed_types(instance=pickup, simulation_data=simulation_data)
