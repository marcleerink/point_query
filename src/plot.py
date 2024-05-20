import random

import folium
from rtreelib import Rect, RTree


# Function to generate random small rectangles around the world
def generate_random_small_rectangles(n: int, size: float = 0.1) -> dict[str, Rect]:
    rectangles = {}
    for i in range(n):
        center_x = random.uniform(-90, 90)
        center_y = random.uniform(-180, 180)
        min_x = center_x - size / 2
        max_x = center_x + size / 2
        min_y = center_y - size / 2
        max_y = center_y + size / 2
        rectangles[f"Rect{i}"] = Rect(min_x, min_y, max_x, max_y)
    return rectangles


# Generate random small rectangles
rectangles = generate_random_small_rectangles(500, size=0.3)

# Create R-tree and insert points
t = RTree()

for name, rect in rectangles.items():
    t.insert(name, rect)


# Function to get bounding boxes from the R-tree using levels
def get_bounding_boxes_by_level(tree: RTree) -> list[list[Rect]]:
    bounding_boxes_by_level = []
    for level in tree.get_levels():
        level_bounding_boxes = []
        for node in level:
            level_bounding_boxes.append(node.get_bounding_rect())
        bounding_boxes_by_level.append(level_bounding_boxes)
    return bounding_boxes_by_level


# Get bounding boxes from the R-tree grouped by levels
bounding_boxes_by_level = get_bounding_boxes_by_level(t)

# Count total nodes and entries
total_nodes = sum(len(level) for level in t.get_levels())
total_entries = sum(len(node.entries) for node in t.get_nodes() if node.is_leaf)

# Define colors for visited nodes
colors = [
    "blue",
    "green",
    "purple",
    "orange",
    "darkred",
    "lightred",
    "darkblue",
    "darkgreen",
    "lightgreen",
    "cadetblue",
    "pink",
    "lightgray",
    "black",
]

# Simulate a query and note the bounding boxes it has to visit
query_bbox = Rect(-10, 35, 30, 60)
visited_nodes = list(t.query_nodes(query_bbox, leaves=False))
found_entries = list(t.query(query_bbox))

# Create a Folium map centered at a midpoint
m = folium.Map(location=[20, 0], zoom_start=2)

# Add total entries layer (make this visible by default)
total_entries_layer = folium.FeatureGroup(
    name=f"Total Entries ({total_entries} entries)", show=True
)
for node in t.get_nodes():
    if node.is_leaf:
        for entry in node.entries:
            bbox = entry.rect
            folium.Rectangle(
                bounds=[[bbox.min_x, bbox.min_y], [bbox.max_x, bbox.max_y]],
                color="green",
                fill=False,
            ).add_to(total_entries_layer)
total_entries_layer.add_to(m)

# Add bounding boxes to the map grouped by levels
for level_idx, bounding_boxes in enumerate(bounding_boxes_by_level):
    color = colors[level_idx % len(colors)]
    feature_group = folium.FeatureGroup(
        name=f"Level {level_idx} ({len(bounding_boxes)} rectangles)", show=False
    )
    for bbox in bounding_boxes:
        folium.Rectangle(
            bounds=[[bbox.min_x, bbox.min_y], [bbox.max_x, bbox.max_y]],
            color=color,
        ).add_to(feature_group)
    feature_group.add_to(m)

# Add query bounding box to the map (make this the second visible layer)
query_layer = folium.FeatureGroup(name="Query Bounding Box", show=False)
folium.Rectangle(
    bounds=[[query_bbox.min_x, query_bbox.min_y], [query_bbox.max_x, query_bbox.max_y]],
    color="red",
    fill=False,
).add_to(query_layer)
query_layer.add_to(m)

# Add visited nodes layer, separating them by order of visit
for idx, node in enumerate(visited_nodes):
    visited_layer = folium.FeatureGroup(name=f"Visited Node {idx + 1}", show=False)
    color = colors[idx % len(colors)]
    bbox = node.get_bounding_rect()
    folium.Rectangle(
        bounds=[[bbox.min_x, bbox.min_y], [bbox.max_x, bbox.max_y]],
        color=color,
        fill=False,
    ).add_to(visited_layer)
    visited_layer.add_to(m)

# Add found rectangles layer
found_layer = folium.FeatureGroup(
    name=f"Found Rectangles ({len(found_entries)} rectangles)", show=False
)
for entry in found_entries:
    bbox = entry.rect
    folium.Rectangle(
        bounds=[[bbox.min_x, bbox.min_y], [bbox.max_x, bbox.max_y]],
        color="green",
        fill=True,
        fill_opacity=1,
    ).add_to(found_layer)
found_layer.add_to(m)

# Add layer control to toggle the visibility of each layer and markers
folium.LayerControl().add_to(m)

# Save the map to an HTML file
m.save("docs/plots/rtree_map.html")
