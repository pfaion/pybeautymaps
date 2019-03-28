import overpy

api = overpy.Overpass()

# fetch all ways and nodes
result = api.query("""
    way(50.746,7.154,50.748,7.157) ["highway"];
    (._;>;);
    out body;
    """)

for way in result.ways:
    print("Name: %s" % way.tags.get("name", "n/a"))
    print("  Highway: %s" % way.tags.get("highway", "n/a"))
    print("  Nodes:")
    for node in way.nodes:
        print("    Lat: %f, Lon: %f" % (node.lat, node.lon))

# %% test
from PIL import Image, ImageDraw
im = Image.new("RGB", (800, 600), "white")
draw = ImageDraw.Draw(im)
draw.arc([10, 40, 100, 200], 20, 90, "green")
del draw
im.show()
