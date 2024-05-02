import random

import folium
from folium import GeoJson, Marker
from rtreelib import Rect, RTree
from shapely.geometry import box, mapping


def generate_random_points(num_points, lat_range=(-90, 90), lon_range=(-180, 180)):
    points = {}
    for i in range(num_points):
        lat = random.uniform(*lat_range)
        lon = random.uniform(*lon_range)
        points[f"Point {i}"] = (lon, lat)
    return points


# Initialize and populate the RTree with points

rtree = RTree()
points = generate_random_points(50)
for name, point in points.items():
    rtree.insert(data=name, rect=Rect(point[0], point[0], point[1], point[1]))


# europe bbox
query_bbox = Rect(-10, 35, 30, 60)
results = rtree.query_nodes(query_bbox)


m = folium.Map(
    location=[
        (query_bbox.min_x + query_bbox.min_y) / 2,
        (query_bbox.max_x + query_bbox.max_y) / 2,
    ],
    zoom_start=5,
)

for node in rtree.get_nodes():
    geojson = {"type": "Feature", "geometry": None, "properties": None}
    rect = node.get_bounding_rect()
    geojson["geometry"] = mapping(box(rect.min_x, rect.min_y, rect.max_x, rect.max_y))

    GeoJson(
        geojson,
        style_function=lambda x: {"color": "grey", "weight": 0.5, "dashArray": "5, 5"},
    ).add_to(m)

# Add points to the map
for name, point in points.items():
    Marker([point[1], point[0]], popup=name).add_to(m)

# Highlight results

for node in results:
    for result in node.entries:
        if not result.is_leaf:
            raise ValueError("supposed to be a leaf")
        Marker(
            [result.rect.min_y, result.rect.min_x],
            icon=folium.Icon(color="green"),
            popup=f"Result: {result.data}",
        ).add_to(m)

# Add the query box as a GeoJson object
folium.GeoJson(
    mapping(
        box(query_bbox.min_x, query_bbox.min_y, query_bbox.max_x, query_bbox.max_y)
    ),
    name="Query Box",
    style_function=lambda x: {"color": "red", "weight": 2},
).add_to(m)


# Add layer control and display the map
folium.LayerControl().add_to(m)
m.save("docs/plots/rtree_map_optimized.html")
