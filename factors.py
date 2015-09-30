"""The following factor functions take two homes as input and return the unnormalized similarity factor values.
This module is extensible and reusable. Users can add new factors easily without affecting the existing code."""
import math


def location_factor(p, q):
    """
    The inverse distance between two locations:
    location_factor = 1 / (sqrt((p.lon - q.lon) ^ 2 + (p.lat - q.lat) ^ 2) + 1) (here add 1 for smoothing)
    continuous variable, range = [0, 1], the larger the factor, the higher the similarity
    """
    return 1 / (math.sqrt((p.lon - q.lon)**2 + (p.lat - q.lat)**2) + 1)


def bedrooms_factor(p, q):
    """
    discrete variable
    diff = p.num_bedrooms - q.num_bedrooms
    switch (diff):
        case 0: bedroom_factor = 1
        case 1: bedroom_factor = 0.5
        case >= 2: bedroom_factor = 0
    """
    diff = p.num_bedrooms - q.num_bedrooms
    if diff == 0:
        return 1
    elif diff == 1:
        return 0.5
    else:
        return 0


def bathrooms_factor(p, q):
    """similiar with bedrooms_factor"""
    diff = p.num_bathrooms - q.num_bathrooms
    if diff == 0:
        return 1
    elif diff == 1:
        return 0.5
    else:
        return 0


def dwelling_type_factor(p, q):
    if p.dwelling_type == q.dwelling_type:
        return 1
    else:
        return 0


def living_area_factor(p, q):
    """The inverse living_area difference"""
    return 1.0 / (abs(p.living_area - q.living_area) + 1)


def pool_factor(p, q):
    if p.pool == q.pool:
        return 1
    elif p.pool == 'none' or q.pool == 'none':
        return 0
    else:
        return 0.3


def list_price_factor(p, q):
    """The inverse list_price difference"""
    return 1.0 / (abs(p.list_price - q.list_price) + 1)
