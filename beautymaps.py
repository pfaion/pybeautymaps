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

        self.road_data = [
            way.tags.get('highway', '')
            for way in self.raw_overpass_data
        ]

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


    def render_square_png(self, filename, size, padding, line_widths=dict()):
        # 2D float
        coord_min = np.min([way.min(axis=0) for way in self.cathographic_data], axis=0)
        coord_max = np.max([way.max(axis=0) for way in self.cathographic_data], axis=0)
        coord_range = coord_max - coord_min

        scale = size / coord_range.min()

        with cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size) as surface:
            ctx = cairo.Context(surface)
            ctx.scale(1, 1)

            # white background
            ctx.rectangle(0, 0, size, size)
            ctx.set_source_rgb(1, 1, 1)
            ctx.fill()

            ctx.set_source_rgb(0, 0, 0)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            for way, road_type in zip(self.cathographic_data, self.road_data):
                ctx.set_line_width(line_widths.get(road_type, 1))
                way_zeroed = np.rint((way - coord_min) * scale).astype(int)
                x, y = way_zeroed[0, :]
                ctx.move_to(x, size - y)
                for x, y in way_zeroed[1:]:
                    ctx.line_to(x, size - y)
                ctx.stroke()

            # padding
            ctx.set_source_rgb(1, 1, 1)
            padding_rects = [
                (0, 0, size, padding),
                (0, 0, padding, size),
                (size - padding, 0, padding, size),
                (0, size - padding, size, padding),
            ]
            for rect in padding_rects:
                ctx.rectangle(*rect)
                ctx.fill()

            surface.write_to_png(filename)


line_widths = dict(
    trunk=5,
    primary=4,
    secondary=3,
    tertiary=2,
)
m = Beautymap.centered(center_latlon=(57.538498, 25.412396), size=1.2)
m.render_square_png("test.png", size=2000, padding=50, line_widths=line_widths)
