# Geospatial Query Optimization for Mapping Applications

## Introduction to the Problem

### Objective

This portfolio focuses on optimizing geospatial queries to efficiently retrieve point data in a mapping application that predicts plastic locations. The goal is to find and display relevant data within user-defined viewports (bounding boxes) quickly and effectively.

### Challenges

The main challenges include:

- Managing and querying large datasets of geospatial plastic predictions.
- Ensuring the application remains performant and responsive even as users change their viewport.

## Theoretical Background

### Basic Algorithm

Initially, one might consider a simple **linear search** through an unsorted list of points within the dataset. While straightforward, this method is inefficient for large datasets.

### R-tree Index Algorithm

To address the inefficiencies of the basic approach, the R-tree, a spatial data structure, is introduced. R-trees are ideal for indexing large amounts of spatial data and support efficient querying of multi-dimensional information. By organizing points into a hierarchical structure, R-trees can significantly reduce the number of points that need to be checked against a given query bounding box.

## Detailed Algorithmic Analysis with Python Code Examples

### Basic Linear Search Algorithm

**Procedure**: Check each point against the bounding box to determine if it should be displayed.

**Python Code Example**:

```python
def linear_search(points, bbox):
    results = []
    for point in points:
        if bbox[0] <= point[0] <= bbox[2] and bbox[1] <= point[1] <= bbox[3]:
            results.append(point)
    return results
```

**Time Complexity Analysis:**

Every point n in the dataset must be checked individually against the query bounding box. This results in a linear time complexity of O(n) for best, average, and worst-case scenarios.

### R-tree Indexing Algorithm

Procedure: Utilize the hierarchical structure of R-trees to avoid unnecessary checks by excluding entire groups of points that do not intersect with the bounding box.

**Python Code Example**: [r_tree.py](../src/r_tree.py)

**Time Complexity Analysis:**

**Insertion (`insert` method)**

- **Process**: The insertion process involves finding the appropriate leaf node and updating or splitting the node if necessary.
- **Complexity**:
  - **Best Case**: If the tree is shallow (which isn't typical unless there's little data), the insertion is O(1) because it directly inserts into the root or a close child.
  - **Average Case**: Assuming a reasonably balanced tree, the complexity of finding the right node to insert into, given by the height of the tree, is O(log⁡ n). However, this is under the assumption that the tree remains balanced without explicit rebalancing logic, which may not always be the case.
  - **Worst Case**: In a poorly balanced tree, particularly where nodes have skewed distributions that cause unbalanced splits, the complexity could degrade to O(n). This situation could arise if splits consistently occur in a way that one side always receives more entries than the other.

**Query (`query` method)**

- **Process**: The query operation checks each node starting from the root to see if the query box intersects with the node’s bounding box and recursively checks its children if it does.
- **Complexity**:
  - **Best Case**: If the query region directly targets a sparsely populated or well-separated part of the space that few nodes cover, the complexity could be as low as O(log⁡ n), because it quickly narrows down to a specific area.
  - **Average Case**: For well-distributed data in a balanced tree, the complexity should ideally be O(log⁡ n)because each level of the tree exponentially decreases the number of potential intersecting nodes.
  - **Worst Case**: If the query intersects with many or all bounding boxes (e.g., a very large query box in a densely populated tree), or if the tree is poorly balanced with lots of overlap, the complexity could go up to O(n). This would occur if nearly every node needs to be checked.

## Plotting and Visualizing the Results

I've included a interactive map that visualizes the results of a query and hierarchical bounding box structure of the R-tree in a real-world scenario. The map is generated using the `folium` library.
[map](plots/rtree_map_optimized.html)

## References

- S. Brakatsoulas, D. Pfoser, and Y. Theodoridis. "Revisiting R-Tree Construction Principles", Advances in Databases and Information Systems 2435 (2002)

- Leutenegger, Scott T.; Edgington, Jeffrey M.; Lopez, Mario A. (February 1997). “STR: A Simple and Efficient Algorithm for R-Tree Packing”. https://ia600900.us.archive.org/27/items/nasa_techdoc_19970016975/19970016975.pdf