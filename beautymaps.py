# %% mercator projection helper functions
import math

def merc_x(lon):
    r_major=6378137.000
    return r_major*math.radians(lon)

def merc_y(lat):
    if lat>89.5:lat=89.5
    if lat<-89.5:lat=-89.5
    r_major=6378137.000
    r_minor=6356752.3142
    temp=r_minor/r_major
    eccent=math.sqrt(1-temp**2)
    phi=math.radians(lat)
    sinphi=math.sin(phi)
    con=eccent*sinphi
    com=eccent/2
    con=((1.0-con)/(1.0+con))**com
    ts=math.tan((math.pi/2-phi)/2)/con
    y=0-r_major*math.log(ts)
    return y

def project(lat, lon, **kwargs):
    return merc_x(lon), merc_y(lat)

 # %% overpy test
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


# %% convert ways to x/y
inf = float("inf")
xrange = (inf, -inf)
yrange = (inf, -inf)
pixelways = []
for way in result.ways:
    tmp = []
    for node in way.nodes:
        x, y = project(**node.__dict__)
        xrange = (min(xrange[0], x), max(xrange[1], x))
        yrange = (min(yrange[0], y), max(yrange[1], y))
        tmp.append((x, y))
    pixelways.append(tmp)

for i, way in enumerate(pixelways):
    for j, (x, y) in enumerate(way):
        pixelways[i][j] = (x - xrange[0], y - yrange[0])

width = math.ceil(xrange[1] - xrange[0])
height = math.ceil(yrange[1] - yrange[0])

# %% test print w cairo
import cairo

with cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height) as surface:
    context = cairo.Context(surface)
    context.scale(1, 1)
    context.set_source_rgb(0, 0, 0)
    context.set_line_width(1)
    for way in pixelways:
        x, y = way[0]
        context.move_to(int(x), int(y))
        for x, y in way:
            context.line_to(int(x), int(y))
    context.stroke()

    surface.write_to_png("example.png")
