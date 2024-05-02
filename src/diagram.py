from rtreelib import Rect, RTree
from rtreelib.diagram import create_rtree_diagram

# Create an RTree instance with some sample data
t = RTree(max_entries=4)

# real world point data of cities
rectangles = {
    "New York": Rect(40.7128, -74.0060, 40.7128, -74.0060),
    "Los Angeles": Rect(34.0522, -118.2437, 34.0522, -118.2437),
    "Chicago": Rect(41.8781, -87.6298, 41.8781, -87.6298),
    "Houston": Rect(29.7604, -95.3698, 29.7604, -95.3698),
    "Phoenix": Rect(33.4484, -112.0740, 33.4484, -112.0740),
    "Berlin": Rect(52.5200, 13.4050, 52.5200, 13.4050),
    "Paris": Rect(48.8566, 2.3522, 48.8566, 2.3522),
    "London": Rect(51.5074, -0.1278, 51.5074, -0.1278),
    "Rome": Rect(41.9028, 12.4964, 41.9028, 12.4964),
    "Melbourne": Rect(-37.8136, 144.9631, -37.8136, 144.9631),
    "Sydney": Rect(-33.8688, 151.2093, -33.8688, 151.2093),
    "Cape Town": Rect(-33.9249, 18.4241, -33.9249, 18.4241),
}
for city, rect in rectangles.items():
    t.insert(city, rect)


# Create a diagram of the R-tree structure
create_rtree_diagram(t)
