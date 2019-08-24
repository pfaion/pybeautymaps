import cairo
import numpy as np
import overpy

from . import utils


class Beautymap:

    @classmethod
    def square_centered(cls, center_latlon, width):
        bbox = utils.bbox_from_centered(center_latlon, width)
        return cls(bbox)

    def __init__(self, bbox):
        self.bbox = bbox
        bbox_data = np.array(self.bbox).reshape((2, 2))
        self.carthographic_bbox = utils.carthographic_from_geodetic(bbox_data)[0]

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

        self.carthographic_data = utils.carthographic_from_geodetic(*self.geodetic_data)

    def get_overpass_data(self):
        self.overpass_ql_query = f"""
            (
            way
                // filter road types with OR regex
                ["highway"~"^{'|'.join(self.road_types)}$"]
                {str(self.bbox)};
                >;
            );
            out;
        """
        return overpy.Overpass().query(self.overpass_ql_query).ways

    def render_square_png(self, filename, size, padding, line_widths=dict()):
        coord_min = self.carthographic_bbox[0, :]
        coord_max = self.carthographic_bbox[1, :]
        coord_range = coord_max - coord_min

        px_per_coord = (size - 2 * padding) / coord_range.min()

        # offsets for non-square shaped bounding boxes
        offset = (coord_range - coord_range.min()) / 2

        with cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size) as surface:
            ctx = cairo.Context(surface)
            ctx.scale(1, 1)

            # white background
            ctx.rectangle(0, 0, size, size)
            ctx.set_source_rgb(1, 1, 1)
            ctx.fill()

            ctx.set_source_rgb(0, 0, 0)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            for way, road_type in zip(self.carthographic_data, self.road_data):
                ctx.set_line_width(line_widths.get(road_type, 1))
                way_zeroed = (way - coord_min - offset) * px_per_coord + padding
                way_zeroed = np.rint(way_zeroed).astype(int)
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


if __name__ == "__main__":
    m = Beautymap.square_centered((40.757667, -73.983715), 8.0)
    m.render_square_png(
        filename='test.png',
        size=2000,
        padding=50,
        line_widths={
            'trunk': 5,
            'primary': 4,
            'secondary': 3,
            'tertiary': 2,
        }
    )
