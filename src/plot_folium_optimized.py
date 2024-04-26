import random

import folium
from folium import GeoJson, Marker
from rtree import index
from shapely.geometry import box, mapping


def generate_random_points(num_points, lat_range=(-90, 90), lon_range=(-180, 180)):
    points = {}
    for i in range(num_points):
        lat = random.uniform(*lat_range)
        lon = random.uniform(*lon_range)
        points[f"Point {i}"] = (lon, lat)
    return points


# Initialize and populate the RTree with points
p = index.Property()
p.dimension = 2
rtree = index.Index()
points = generate_random_points(200)
i = 0
for name, point in points.items():
    rtree.insert(id=i, coordinates=point, obj=name)
    i += 1


# europe bbox
query_bbox = (-10, 35, 30, 60)
results = rtree.intersection(query_bbox, objects=True)


m = folium.Map(
    location=[(query_bbox[1] + query_bbox[3]) / 2, (query_bbox[0] + query_bbox[2]) / 2],
    zoom_start=5,
)

for node in rtree.leaves():
    geojson = {"type": "Feature", "geometry": None, "properties": None}
    geojson["geometry"] = mapping(box(*node[2]))

    GeoJson(
        geojson,
        style_function=lambda x: {"color": "grey", "weight": 1, "dashArray": "5, 5"},
    ).add_to(m)

# Add points to the map
for name, point in points.items():
    Marker([point[1], point[0]], popup=name).add_to(m)

# Highlight results
for result in results:
    print(result.bbox, result.object)
    Marker(
        [result.bbox[1], result.bbox[0]],
        icon=folium.Icon(color="green"),
        popup=f"Result: {result.object}",
    ).add_to(m)

# Add the query box as a GeoJson object
folium.GeoJson(
    mapping(box(*query_bbox)),
    name="Query Box",
    style_function=lambda x: {"color": "red", "weight": 2},
).add_to(m)


# Add layer control and display the map
folium.LayerControl().add_to(m)
m.save("docs/plots/rtree_map_optimized.html")
