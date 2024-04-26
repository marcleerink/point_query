import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, box

from src.r_tree import RTree

# Assuming your RTree and Node classes are properly imported and set up

# Initialize and populate the RTree with points
rtree = RTree()
points = {
    "Berlin": (13.4050, 52.5200),
    "Paris": (2.3522, 48.8566),
    "London": (-0.1276, 51.5074),
    "New York": (-74.0060, 40.7128),
    "Los Angeles": (-118.2437, 34.0522),
    "Mexico City": (-99.1332, 19.4326),
    "Toronto": (-79.3832, 43.6532),
    "Sydney": (151.2093, -33.8688),
    "Tokyo": (139.6917, 35.6895),
    "Moscow": (37.6173, 55.7558),
}

for point in points.values():
    rtree.insert(point)

# query to just include Berlin
query_bbox = (13.0, 52.0, 14.0, 53.0)

# Query the R-tree
results = rtree.query(query_bbox)

# Convert points and bounding box to GeoDataFrame
gdf = gpd.GeoDataFrame(
    geometry=[Point(lon, lat) for lon, lat in points.values()], crs="EPSG:4326"
)
query_gdf = gpd.GeoDataFrame(geometry=[box(*query_bbox)], crs="EPSG:4326")
results_gdf = gpd.GeoDataFrame(
    geometry=[Point(lon, lat) for lon, lat in results], crs="EPSG:4326"
)

# Plotting setup
fig, ax = plt.subplots(figsize=(10, 10))
gdf.to_crs(epsg=3857).plot(ax=ax, color="blue", marker="o", label="Cities")
query_gdf.to_crs(epsg=3857).boundary.plot(ax=ax, color="red", label="Query Box")
results_gdf.to_crs(epsg=3857).plot(
    ax=ax, color="green", marker="x", label="Query Results"
)

# Visualize all node bounds in the R-tree
for node in rtree.all_nodes():
    print(node.bounds)
    node_bounds = gpd.GeoDataFrame(geometry=[box(*node.bounds)], crs="EPSG:4326")
    node_bounds.to_crs(epsg=3857).boundary.plot(
        ax=ax,
        color="grey",
        linestyle="--",
        label="Node Bounds" if "node_bounds_legend" not in locals() else "",
    )

ax.set_title("R-Tree Visualization with Real-World Map")

ax.set_axis_off()
ax.legend()
plt.show()
