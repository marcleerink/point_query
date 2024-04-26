# Self-reflection

## Marc Leerink, SE_02 Algorithms and Data Structures, 26 April 2024, Semester 6

This semester I've worked on the Ocean Eco Watch project.
Ocean Eco Watch is a open-source project that aims to provide a web mapping application that displays marine debris in coastal areas. The project is funded by the Prototype fund.

One challenge we faced was keeping our mapping application performant with a large amount of vector point data. We need to efficiently retrieve and display plastic predictions within user-defined viewports (bounding boxes). Traditional database indexing methods based on binary trees are not sufficient due to the multi-dimensional nature of geospatial data.

To address this challenge I researched and implemented a R-tree datastructure. By organizing points into a hierarchical structure, R-trees can significantly reduce the number of points that need to be checked against a given query bounding box.

My implementation is far from perfect, but it's a good start. I've implemented the insertion method of the R-tree and added a basic query method. The most complex part is keeping the tree balanced by splitting nodes correctly when they reach the max_children limit. My first implementation was a simple recursive split method, but I've learned that this is not the most efficient way to split nodes. I've started to implement splitting logic based on the [R\*-tree algorithm](references/r-tree-clustering-split-algo.pdf). This splitting logic evaluates the best split based on the overlap and area of the resulting nodes for each axis. This results in a more balanced tree and better query performance.

To show the R-tree in action in a real-world scenario I've added a folium map that displays the R-tree nodes and the points in the nodes. This visualization helped me understand the splitting logic better and see the performance improvements of the R-tree compared to a linear search.
My implementation is far from optimized and if you analyze the difference between the [rtree_map_simple.html](plots/rtree_map_simple.html) and the [rtree_map_optimized.html](plots/rtree_map_optimized.html) you can see that the optimized version has a more balanced tree and less overlap between nodes. The latter has been made with a existing library, which I used as a reference for my own implementation.

In the future I want to optimize the insert and query methods further by experimenting with different
splitting strategies and max_children values. I also want to add more query methods like range queries and nearest neighbor queries.

Overall, I've learned a lot about spatial data structures and how they can be used to optimize geospatial queries. I've also learned that implementing a complex data structure like a R-tree is not easy and requires a lot of research and experimentation. However, in relation to this module, this project has helped me to make the abstract concepts of algorithms and data structures more concrete. I'm happy with the progress I've made and I'm looking forward to further optimizing my implementation and integrating it into the Ocean Eco Watch project.
