import random

import graphviz
from rtreelib import Rect, RTree, RTreeEntry


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
rectangles = generate_random_small_rectangles(10, size=1.0)

# Create R-tree and insert points
t = RTree()

for name, rect in rectangles.items():
    t.insert(name, rect)


# Function to create a hierarchical diagram of the R-tree
def create_rtree_diagram(tree: RTree, filename: str):
    dot = graphviz.Digraph()

    # Recursive function to add nodes and edges to the graph
    def add_node(dot, node, parent=None):
        node_id = id(node)
        if node.is_leaf:
            node_label = "|".join([str(entry.data) for entry in node.entries])
        else:
            node_label = "|".join(["" for _ in node.entries])

        dot.node(str(node_id), label=node_label, shape="record")
        if parent:
            dot.edge(str(parent), str(node_id))

        if not node.is_leaf:
            for entry in node.entries:
                if isinstance(entry, RTreeEntry) and entry.child:
                    add_node(dot, entry.child, node_id)

    # Start with the root node
    add_node(dot, tree.root)

    # Save the diagram
    dot.render(filename, format="png", cleanup=True)


# Create the R-tree diagram
create_rtree_diagram(t, "rtree_diagram")
