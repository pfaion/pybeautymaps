import math

import numpy as np
from pyproj import Proj


def is_valid_latitude(lat):
    return -90 <= lat <= 90


def is_valid_longitude(lon):
    return -180 <= lon <= 180


def bbox_from_centered(center_latlon, width):
    if width <= 0:
        raise ValueError(f'Bounding box width must be positive! Is: {width}')

    lat, lon = center_latlon
    if not is_valid_latitude(lat):
        raise ValueError(f'Latitude needs to be in [-90, 90]! Is: {lat}')
    if not is_valid_longitude(lon):
        raise ValueError(f'Longitude needs to be in [-180, 180]! Is: {lon}')

    # quick and dirty conversion of cathographic to geodetic distances
    # see: https://gis.stackexchange.com/a/2964
    # TODO: use pyproj for this as well!
    delta_lat = width / 111.111
    delta_lon = abs(width / (111.111 * math.cos(lat)))
    bbox = (lat - delta_lat, lon - delta_lon, lat + delta_lat, lon + delta_lon)
    return bbox


def carthographic_from_geodetic(*latlons):
    # EPSG.3857 projection https://epsg.io/3857
    # Pseudo-Mercator as used by Google Maps and Open Street Maps
    proj = Proj(3857)
    return [
        # projector works with separate arrays of longs and lats (!)
        np.vstack(proj(coordinates[:, 1], coordinates[:, 0])).T
        for coordinates in latlons
    ]
