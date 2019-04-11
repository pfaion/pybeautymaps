import math

import cairo
import numpy as np
import overpy
from pyproj import Proj


class Beautymap:

    @staticmethod
    def bbox_from_centered(center_latlon, size):
        # quick and dirty conversion of cathographic to geodetic distances
        # see: https://gis.stackexchange.com/a/2964
        # TODO: use pyproj for this as well!
        lat, lon = center_latlon
        delta_lat = size / 111.111
        delta_lon = size / (111.111 * math.cos(lat))
        bbox = (lat - delta_lat, lon - delta_lon, lat + delta_lat, lon + delta_lon)
        return bbox


    @classmethod
    def centered(cls, center_latlon, size):
        bbox = cls.bbox_from_centered(center_latlon, size)
        return cls(bbox)


    def __init__(self, bbox):
        self.bbox = bbox
        self.road_types = {
            'motorway',
            'trunk',
            'primary',
            'secondary',
            'tertiary',
            'residential',
            'living_street',
        }

        self.raw_overpass_data = self.get_overpass_data()

        self.geodetic_data = [
            np.array([(node.lat, node.lon) for node in way.nodes], dtype=float)
            for way in self.raw_overpass_data
        ]

        # EPSG.3857 projection https://epsg.io/3857
        # Pseudo-Mercator as used by Google Maps and Open Street Maps
        proj = Proj(3857)
        self.cathographic_data = [
            # projector works with separate arrays of longs and lats (!)
            np.vstack(proj(way[:, 1], way[:, 0])).T
            for way in self.geodetic_data
        ]

        self.minimum = np.min([way.min(axis=0) for way in self.cathographic_data], axis=0)
        self.maximum = np.max([way.max(axis=0) for way in self.cathographic_data], axis=0)
        self.range = self.maximum - self.minimum

        self.normalized_data = [
            (way - self.minimum)
            for way in self.cathographic_data
        ]


    def get_overpass_data(self):
        overpass_ql_query = f"""
            (
            way
                // filter road types with OR regex
                ["highway"~"^{'|'.join(self.road_types)}$"]
                {str(self.bbox)};
                >;
            );
            out;
        """
        return overpy.Overpass().query(overpass_ql_query).ways


    def render_png(self, filename):
        width, height = np.rint(self.range).astype(int)

        with cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height) as surface:
            ctx = cairo.Context(surface)
            ctx.scale(1, 1)
            ctx.rectangle(0, 0, width, height)
            ctx.set_source_rgb(1, 1, 1)
            ctx.fill()
            ctx.set_source_rgb(0, 0, 0)
            ctx.set_line_width(1)
            for way in self.normalized_data:
                int_way = np.rint(way).astype(int)
                x, y = int_way[0, :]
                ctx.move_to(x, height - y)
                for x, y in int_way[1:]:
                    ctx.line_to(x, height - y)
            ctx.stroke()

            surface.write_to_png(filename)


if __name__ == '__main__':
    m = Beautymap.centered(center_latlon=(57.538498, 25.412396), size=1)
    m.render_png("test.png")
