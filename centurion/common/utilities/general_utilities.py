

# Imports for hashes
from ctypes import c_uint64
from base64 import urlsafe_b64encode
# Imports for get_all_related_objects
from django.db.models.fields.related import ForeignObjectRel
# imports for get_parent_instance
from django.core.exceptions import FieldDoesNotExist
from django.db import models


def calculate_hash(input_string):

    # See https://stackoverflow.com/questions/21999983/fast-hash-for-strings
    return c_uint64(hash(input_string)).value.to_bytes(8,"big").hex()


def get_all_related_objects(instance, models_to_ignore = []):

    # init return related objects
    related_objects = []

    # lazy load the delivery binding to prevent circular imports
    from scenarios.models.delivery import Delivery

    # Select related for problematic fields such as deliveries and whatever our forgen equivalent is
    instance_type = instance._meta.model.__name__
    if instance_type == 'Scenario':

        # tell the select related to ignore these preselected ones
        models_to_ignore.extend(['Order', 'Pickup', 'Delivery'])

        # preselect deliveries
        deliveries = Delivery.objects.select_related(
            'pickup',  # Joins Delivery to Pickup
            'pickup__order',  # Joins Pickup to Order through Delivery
            'pickup__order__scenario'  # Joins Order to Scenario through Pickup and Delivery
        ).filter(
            pickup__order__scenario_id=instance.id  # Filters based on scenario_id
        )
        
        # iterate through
        order_id = 0
        pickup_id = 0
        for delivery in deliveries:
            related_objects.append(delivery)
            if delivery.pickup.id != pickup_id:
                related_objects.append(delivery.pickup)
                pickup_id = delivery.pickup.id
            if delivery.pickup.order.id != order_id:
                related_objects.append(delivery.pickup.order)
                order_id = delivery.pickup.order.id


    # iterate through all the fields of the model
    for field in instance._meta.get_fields():
        
        # check if this is foreign key
        if isinstance(field, ForeignObjectRel):

            # get the related name/model name
            related_name = field.get_accessor_name()
            model_name = field.related_model.__name__

            # ignore instances
            if model_name not in models_to_ignore:

                # use getattr to fetc the object
                related_instances = getattr(instance, related_name).all()

                # Add the related instances to the list
                related_objects.extend(related_instances)

                # recursviely get related objects
                for related_instance in related_instances:
                    related_objects.extend(get_all_related_objects(related_instance, models_to_ignore))

    # finished
    return related_objects


def get_parent_instance(child_instance, parent_model_name):
    """
    Recursively follows foreign key relationships from a child instance to find an instance of the specified parent model.
    
    :param child_instance: The child model instance from which to start.
    :param parent_model_name: The name of the parent model class to find (expected to be the model class name).
    :return: The parent model instance if found, or None if no such parent exists.
    """
    current_instance = child_instance
    visited = set()  # To avoid loops in recursive relationships

    while current_instance:

        # Avoid revisiting the same instance in case of circular relationships
        if current_instance in visited:
            break
        visited.add(current_instance)

        # Check if the current instance is of the type we're looking for
        if current_instance.__class__.__name__.lower() == parent_model_name.lower():
            return current_instance
        
        # Move up to the next related object if possible
        new_instance = None
        for field in current_instance._meta.fields:
            if isinstance(field, models.ForeignKey):
                try:
                    # Try to fetch the related object
                    new_instance = getattr(current_instance, field.name)
                    break
                except FieldDoesNotExist:
                    continue
        
        if new_instance is None:
            # No more foreign keys, stop the search
            return None
        
        # Update the current instance to the newly found related object
        current_instance = new_instance

    return None