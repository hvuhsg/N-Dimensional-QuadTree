# N-Dimensional-QuadTree
Full python implementation of n dimensional quadtree

Example:
```python
from quadtree import NQTree, DataPoint, Point, Cuboid, HyperSphere

# Create the root node
space_dimensions = [
    [0, 100],
    [0, 100],
    [10, 200],
    [100, 300],
]  # Define 4 dimensions space
# for example the x axis is defined from 0 to 100 and the z axis is defined from 10 to 200
t = NQTree(space_dimensions, max_data_points=2)

# Insert data points
t.insert(DataPoint("in circle", Point(15, 18, 20, 115)))
t.insert(DataPoint("in cube", Point(20, 20, 82, 123)))
t.insert(DataPoint("in circle and cube", Point(30, 30, 30, 131)))

# Search shapes
cube = Cuboid(
    min_point=Point(15, 15, 25, 115), max_point=Point(35, 35, 90, 135)
)  # defined by 2 points
# Cuboid is N-dimension rectangle
circle = HyperSphere(center_point=Point(20, 22, 23, 122), radius=20.0)

search_result_cube = t.search(
    cube
)  # -> Return list of points within this shape in O(log n) time
search_result_circle = t.search(circle)  # -> Same just for the HyperSphere

```