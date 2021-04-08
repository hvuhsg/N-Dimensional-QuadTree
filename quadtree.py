
class Point:
    def __init__(self, *args):
        self.dims: list = args
        self.dim_len = len(self.dims)

    def distance(self, other_point):
        sum_count = sum(map(lambda x: (x[0] - x[1]) ** 2, zip(self.dims, other_point.dims)))
        return sum_count ** 0.5

    def copy(self):
        return Point(self.dims)

    def __getitem__(self, dim):
        return self.dims[dim]

    def __setitem__(self, index, value):
        list_dims = list(*self.dims)
        list_dims[index] = value
        self.dims = tuple(list_dims)

    def __copy__(self):
        return self.copy()

    def __iter__(self):
        for dim in self.dims:
            yield dim


class Cuboid:
    def __init__(self, min_point: Point, max_point: Point):
        self.max_point = max_point
        self.min_point = min_point

    def dimensions(self):
        return zip(self.min_point, self.max_point)

    def center_to_edge_length(self):
        diagonal_length = self.min_point.distance(self.max_point)
        return diagonal_length / 2

    def contain(self, point):
        for dim_index, dim_value in enumerate(point):
            if not self.min_point[dim_index] < dim_value or not self.max_point[dim_index] > dim_value:
                return False
        return True

    def __contains__(self, point):
        return self.contain(point)


class HyperSphere:
    def __init__(self, center_point: Point, radius: float):
        self.center_point = center_point
        self.radius = radius

    def dimensions(self):
        return [self.center_point]

    def contain(self, point):
        return self.center_point.distance(point) < self.radius


class DataPoint:
    def __init__(self, value, point: Point):
        self.point = point
        self.value = value


class NQTree(Cuboid):
    def __init__(self, dimensions: list, max_data_points: int, minimum_point: Point = None, maximum_point: Point = None):
        if not (minimum_point and maximum_point):
            minimum_point, maximum_point = self._create_min_max_points(dimensions)
        super().__init__(minimum_point, maximum_point)

        self.dimensions = dimensions
        self.points = []
        self.max_points = max_data_points
        self.childes = []
        self.divided = False

    def _create_min_max_points(self, dimensions):
        return Point(*[dim[0] for dim in dimensions]), Point(*[dim[1] for dim in dimensions])

    def divide(self):
        middle_point = Point(*[(minp + maxp)/2 for minp, maxp in zip(self.min_point, self.max_point)])
        points = [middle_point]
        new_points = []
        for index, dimension in enumerate(self.dimensions):
            for point in points:
                v1 = point.copy()
                v1[index] = point[index] + point[index] / 2
                v2 = point.copy()
                v2[index] = point[index] - point[index] / 2
                new_points.append(v2)
                new_points.append(v1)
                points = new_points
            new_points = []

        childes = []
        for child_middle in points:
            min_point = []
            max_point = []
            for index, dim in enumerate(child_middle):
                if dim > middle_point[index]:
                    min_point.append(middle_point[index])
                    max_point.append(self.max_point[index])
                else:
                    min_point.append(self.min_point[index])
                    max_point.append(middle_point[index])
            childes.append(
                NQTree(
                    self.dimensions,
                    minimum_point=Point(*min_point),
                    maximum_point=Point(*max_point),
                    max_data_points=self.max_points
                )
            )
        self.childes = childes
        self.divided = True

    def insert(self, data_point):
        if not self.contain(data_point.point):
            return False
        if len(self.points) < self.max_points:
            self.points.append(data_point)
            return True
        if not self.divided:
            self.divide()
        return any([child.insert(data_point) for child in self.childes])

    def intersect(self, shape):
        for edge_point in shape.dimensions():
            if self.contain(edge_point):
                return True
        for edge_point in zip(self.min_point, self.max_point):
            if shape.contain(Point(*edge_point)):
                return True
        if isinstance(shape, HyperSphere):
            middle_point = Point(*map(lambda x: (x[0] + x[1]) / 2, zip(self.min_point, self.max_point)))
            if self.center_to_edge_length() + shape.radius < middle_point.distance(shape.center_point):
                return True
        return False

    def search(self, shape):
        if not self.intersect(shape):
            return []
        points = []
        for data_point in self.points:
            if shape.contain(data_point.point):
                points.append(data_point)
        for child in self.childes:
            points.extend(child.search(shape))
        return points

    def __str__(self):
        s = f"NQTree(min={self.min_point}, max={self.max_point}, divided={self.divided}, points={len(self.points)})"
        return s

    def __repr__(self):
        return str(self)

t = NQTree([[0, 100], [0, 100], [10, 200], [100, 300]], max_data_points=2)
t.insert(DataPoint(1, Point(15, 18, 20, 115)))
t.insert(DataPoint(2, Point(20, 20, 82, 123)))
t.insert(DataPoint(3, Point(30, 30, 30, 131)))
cube = Cuboid(Point(15, 15, 25, 115), Point(35, 35, 35, 135))
circle = HyperSphere(Point(20, 22, 23, 122), 20)
search_result = t.search(cube)
search_result_circle = t.search(circle)
