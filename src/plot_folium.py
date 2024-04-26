import random

import folium
from folium import GeoJson, GeoJsonPopup, Marker
from shapely.geometry import box, mapping

from src.r_tree import RTree


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
    rtree.insert(point)


# europe bbox
query_bbox = (-10, 35, 30, 60)
results = rtree.query(query_bbox)

# Create a folium map centered around the middle of the query box
m = folium.Map(
    location=[(query_bbox[1] + query_bbox[3]) / 2, (query_bbox[0] + query_bbox[2]) / 2],
    zoom_start=5,
)

# Add points to the map
for name, point in points.items():
    Marker([point[1], point[0]], popup=name).add_to(m)

# Highlight results
for result in results:
    print(result)
    Marker(
        [result[1], result[0]],
        icon=folium.Icon(color="green"),
        popup=f"Result: {result}",
    ).add_to(m)

# Add the query box as a GeoJson object
folium.GeoJson(
    mapping(box(*query_bbox)),
    name="Query Box",
    style_function=lambda x: {"color": "red", "weight": 2},
).add_to(m)

# Optionally, visualize all node bounds in the R-tree
for node in rtree.all_nodes():
    geojson = {"type": "Feature", "geometry": None, "properties": None}
    geojson["geometry"] = mapping(box(*node.bounds))
    geojson["properties"] = {"is_leaf": node.is_leaf}
    GeoJson(
        geojson,
        popup=GeoJsonPopup(fields=["is_leaf"]),
        style_function=lambda x: {"color": "grey", "weight": 1, "dashArray": "5, 5"},
    ).add_to(m)

# Add layer control and display the map
folium.LayerControl().add_to(m)
m.save("docs/plots/rtree_map_simple.html")
