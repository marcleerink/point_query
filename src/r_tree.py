MAX_CHILDREN = 10


class Node:
    def __init__(self, bounds, max_children=MAX_CHILDREN):
        self.bounds = bounds  # bounds are (min_x, min_y, max_x, max_y)
        self.children = []  # List of points or child nodes
        self.is_leaf = True
        self.max_children = max_children

    def insert(self, point):
        # Update bounds when a new point is inserted
        self.update_bounds(point)
        if self.is_leaf:
            self.children.append(point)
            if len(self.children) > self.max_children:
                self.split()
        else:
            # Insert into child with the least enlargement required
            self.choose_subtree(point).insert(point)

    def split(self):
        # Perform the split on both x and y dimensions and choose the best one
        best_splits = []
        dimensions = [0, 1]

        for dim in dimensions:
            # Sort the children by their dimension value
            self.children.sort(key=lambda child: child[dim])
            # Try splitting at every possible position
            for i in range(1, len(self.children)):
                left = self.children[:i]
                right = self.children[i:]
                bounds1 = self.calculate_bounds(left)
                bounds2 = self.calculate_bounds(right)
                overlap = self.calculate_overlap(bounds1, bounds2)
                area = self.calculate_area(bounds1) + self.calculate_area(bounds2)
                best_splits.append((overlap, area, i, dim))

        # Choose the split with the least overlap, then the least area
        _, _, split_index, split_dim = min(best_splits)
        self.children.sort(key=lambda child: child[split_dim])
        left = self.children[:split_index]
        right = self.children[split_index:]

        # Update the current node with the new children
        self.children = [
            Node(self.calculate_bounds(left), max_children=self.max_children)
        ]
        self.children.append(
            Node(self.calculate_bounds(right), max_children=self.max_children)
        )
        self.is_leaf = False

    def calculate_bounds(self, points):
        min_x = min(p[0] for p in points)
        max_x = max(p[0] for p in points)
        min_y = min(p[1] for p in points)
        max_y = max(p[1] for p in points)
        return (min_x, min_y, max_x, max_y)

    def calculate_overlap(self, bounds1, bounds2):
        min_x1, min_y1, max_x1, max_y1 = bounds1
        min_x2, min_y2, max_x2, max_y2 = bounds2
        overlap_x = max(0, min(max_x1, max_x2) - max(min_x1, min_x2))
        overlap_y = max(0, min(max_y1, max_y2) - max(min_y1, min_y2))
        return overlap_x * overlap_y

    def calculate_area(self, bounds):
        min_x, min_y, max_x, max_y = bounds
        return (max_x - min_x) * (max_y - min_y)

    def update_bounds(self, point):
        px, py = point
        min_x, min_y, max_x, max_y = self.bounds
        if px < min_x:
            min_x = px
        if py < min_y:
            min_y = py
        if px > max_x:
            max_x = px
        if py > max_y:
            max_y = py
        self.bounds = (min_x, min_y, max_x, max_y)

    def choose_subtree(self, point):
        return min(self.children, key=lambda child: child.required_enlargement(point))

    def required_enlargement(self, point):
        px, py = point
        min_x, min_y, max_x, max_y = self.bounds
        enlarged_min_x = min(min_x, px)
        enlarged_min_y = min(min_y, py)
        enlarged_max_x = max(max_x, px)
        enlarged_max_y = max(max_y, py)
        current_area = (max_x - min_x) * (max_y - min_y)
        enlarged_area = (enlarged_max_x - enlarged_min_x) * (
            enlarged_max_y - enlarged_min_y
        )
        return enlarged_area - current_area

    def intersects_point(self, point, bbox):
        px, py = point
        min_x, min_y, max_x, max_y = bbox
        return min_x <= px <= max_x and min_y <= py <= max_y

    def query(self, bbox):
        if not self.intersects(bbox):
            return []
        elif self.is_leaf:
            return [
                child
                for child in self.children
                if bbox[0] <= child[0] <= bbox[2] and bbox[1] <= child[1] <= bbox[3]
            ]
        else:
            results = []
            for child in self.children:
                if child.intersects(bbox):
                    results.extend(child.query(bbox))
            return results

    def intersects(self, bbox):
        node_min_x, node_min_y, node_max_x, node_max_y = self.bounds
        query_min_x, query_min_y, query_max_x, query_max_y = bbox
        return not (
            node_max_x < query_min_x
            or node_min_x > query_max_x
            or node_max_y < query_min_y
            or node_min_y > query_max_y
        )


class RTree:
    def __init__(self, max_children=MAX_CHILDREN):
        self.max_children = max_children
        self.root = None

    def insert(self, point):
        if not self.root:
            self.root = Node(
                (point[0], point[1], point[0], point[1]), max_children=self.max_children
            )
        else:
            self.root.insert(point)
            if len(self.root.children) > self.max_children:  # Check if root was split
                new_root = Node(
                    self.root.calculate_bounds(self.root.children),
                    max_children=self.max_children,
                )
                new_root.children = self.root.children
                new_root.is_leaf = False
                self.root = new_root

    def query(self, bbox):
        if self.root:
            return self.root.query(bbox)
        else:
            return []

    def _all_nodes(self, node):
        if node.is_leaf:
            return [node]
        else:
            return [node] + [
                child for child in node.children for node in self._all_nodes(child)
            ]

    def all_nodes(self):
        return self._all_nodes(self.root)
