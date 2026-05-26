import math
import itertools
from functools import reduce, wraps
from itertools import count, islice, chain
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon


def distance(p1, p2):
    return math.dist(p1, p2)


def polygon_area(poly):
    n = len(poly)

    s = sum(
        poly[i][0] * poly[(i + 1) % n][1]
        - poly[(i + 1) % n][0] * poly[i][1]
        for i in range(n)
    )

    return abs(s) / 2


def polygon_perimeter(poly):
    return sum(
        distance(poly[i], poly[(i + 1) % len(poly)])
        for i in range(len(poly))
    )


def shortest_side(poly):
    return min(
        distance(poly[i], poly[(i + 1) % len(poly)])
        for i in range(len(poly))
    )


def longest_side(poly):
    return max(
        distance(poly[i], poly[(i + 1) % len(poly)])
        for i in range(len(poly))
    )



def visualize(polygons, title="Polygons"):
    fig, ax = plt.subplots(figsize=(10, 8))

    for poly in polygons:
        patch = MplPolygon(poly, fill=False)
        ax.add_patch(patch)

    ax.autoscale()
    ax.set_aspect("equal")
    ax.grid(True)
    plt.title(title)
    plt.show()



def gen_rectangle(width=2, height=1, step=4):
    for i in count():
        x = i * step
        yield (
            (x, 0),
            (x + width, 0),
            (x + width, height),
            (x, height),
        )


def gen_triangle(side=2, step=4):
    h = side * math.sqrt(3) / 2

    for i in count():
        x = i * step
        yield (
            (x, 0),
            (x + side / 2, h),
            (x + side, 0),
        )


def gen_hexagon(radius=1, step=4):
    for i in count():
        cx = i * step

        yield tuple(
            (
                cx + radius * math.cos(math.pi / 3 * k),
                radius * math.sin(math.pi / 3 * k),
            )
            for k in range(6)
        )



def translate_polygon(poly, dx, dy):
    return tuple((x + dx, y + dy) for x, y in poly)


def rotate_polygon(poly, angle_deg):
    angle = math.radians(angle_deg)

    c = math.cos(angle)
    s = math.sin(angle)

    return tuple(
        (
            x * c - y * s,
            x * s + y * c,
        )
        for x, y in poly
    )


def symmetry_polygon(poly, axis="x"):

    if axis == "x":
        return tuple((x, -y) for x, y in poly)

    if axis == "y":
        return tuple((-x, y) for x, y in poly)

    if axis == "origin":
        return tuple((-x, -y) for x, y in poly)

    raise ValueError("axis")


def homothety_polygon(poly, k):
    return tuple((x * k, y * k) for x, y in poly)


def tr_translate(iterator, dx, dy):
    return map(lambda p: translate_polygon(p, dx, dy), iterator)


def tr_rotate(iterator, angle):
    return map(lambda p: rotate_polygon(p, angle), iterator)


def tr_symmetry(iterator, axis="x"):
    return map(lambda p: symmetry_polygon(p, axis), iterator)


def tr_homothety(iterator, k):
    return map(lambda p: homothety_polygon(p, k), iterator)



def is_convex(poly):

    n = len(poly)

    if n < 3:
        return False

    signs = []

    for i in range(n):

        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        x3, y3 = poly[(i + 2) % n]

        cross = (
            (x2 - x1) * (y3 - y2)
            - (y2 - y1) * (x3 - x2)
        )

        if cross != 0:
            signs.append(cross > 0)

    return all(signs) or not any(signs)


def flt_convex_polygon(iterator):
    return filter(is_convex, iterator)


def flt_angle_point(iterator, point):
    return filter(lambda p: point in p, iterator)


def flt_square(iterator, max_area):
    return filter(
        lambda p: polygon_area(p) < max_area,
        iterator
    )


def flt_short_side(iterator, max_side):
    return filter(
        lambda p: shortest_side(p) < max_side,
        iterator
    )


def point_inside_convex(poly, point):
    x, y = point
    n = len(poly)

    sign = None

    for i in range(n):

        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]

        cross = (
            (x2 - x1) * (y - y1)
            - (y2 - y1) * (x - x1)
        )

        if cross == 0:
            continue

        cur = cross > 0

        if sign is None:
            sign = cur

        elif sign != cur:
            return False

    return True


def flt_point_inside(iterator, point):
    return filter(
        lambda p: point_inside_convex(p, point),
        iterator
    )


def flt_polygon_angles_inside(iterator, polygon):

    def check(poly):
        return any(
            point_inside_convex(poly, pt)
            for pt in polygon
        )

    return filter(check, iterator)



def decorator_filter(filter_func, *args):

    def outer(func):

        @wraps(func)
        def wrapper(*fargs, **fkwargs):

            result = func(*fargs, **fkwargs)

            return filter_func(result, *args)

        return wrapper

    return outer


def decorator_transform(transform_func, *args):

    def outer(func):

        @wraps(func)
        def wrapper(*fargs, **fkwargs):

            result = func(*fargs, **fkwargs)

            return transform_func(result, *args)

        return wrapper

    return outer



def agr_origin_nearest(iterator):

    return reduce(
        lambda a, b:
        a if min(math.dist((0, 0), p) for p in a)
        <
        min(math.dist((0, 0), p) for p in b)
        else b,
        iterator
    )


def agr_max_side(iterator):

    return reduce(
        lambda a, b:
        a if longest_side(a) > longest_side(b)
        else b,
        iterator
    )


def agr_min_area(iterator):

    return reduce(
        lambda a, b:
        a if polygon_area(a) < polygon_area(b)
        else b,
        iterator
    )


def agr_perimeter(iterator):

    return reduce(
        lambda acc, p:
        acc + polygon_perimeter(p),
        iterator,
        0
    )


def agr_area(iterator):

    return reduce(
        lambda acc, p:
        acc + polygon_area(p),
        iterator,
        0
    )



def zip_polygons(*iterators):

    for polygons in zip(*iterators):
        yield tuple(chain.from_iterable(polygons))



def count_2D():
    for x in count():
        for y in count():
            yield (x, y)


def zip_tuple(*tuples_):
    return tuple(chain.from_iterable(tuples_))



if __name__ == "__main__":

    rects = list(islice(gen_rectangle(), 7))
    tris = list(islice(gen_triangle(), 7))
    hexs = list(islice(gen_hexagon(), 7))

    visualize(rects, "Rectangles")
    visualize(tris, "Triangles")
    visualize(hexs, "Hexagons")
  
    base = islice(gen_rectangle(), 7)

    ribbon1 = list(
        tr_rotate(
            tr_translate(base, 0, 0),
            25
        )
    )

    ribbon2 = list(
        tr_rotate(
            tr_translate(
                islice(gen_rectangle(), 7),
                0,
                5
            ),
            25
        )
    )

    ribbon3 = list(
        tr_rotate(
            tr_translate(
                islice(gen_rectangle(), 7),
                0,
                10
            ),
            25
        )
    )

    visualize(
        ribbon1 + ribbon2 + ribbon3,
        "Three ribbons"
    )


    r1 = list(
        tr_rotate(
            islice(gen_rectangle(), 7),
            30
        )
    )

    r2 = list(
        tr_translate(
            tr_rotate(
                islice(gen_rectangle(), 7),
                -30
            ),
            5,
            5
        )
    )

    visualize(r1 + r2, "Intersecting ribbons")


    t1 = list(
        tr_translate(
            islice(gen_triangle(), 7),
            0,
            4
        )
    )

    t2 = list(
        tr_symmetry(
            tr_translate(
                islice(gen_triangle(), 7),
                0,
                4
            ),
            "x"
        )
    )

    visualize(t1 + t2, "Symmetric triangles")

    quads = [
        homothety_polygon(
            next(gen_rectangle()),
            k
        )
        for k in range(1, 16)
    ]

    visualize(quads, "Homothety")

    filtered = list(
        flt_short_side(
            iter(quads),
            3
        )
    )

    print("Filtered:", len(filtered))

    sample = list(islice(gen_rectangle(), 10))

    print(
        "Total area:",
        agr_area(iter(sample))
    )

    print(
        "Total perimeter:",
        agr_perimeter(iter(sample))
    )

    print(
        "Min area:",
        polygon_area(
            agr_min_area(iter(sample))
        )
    )

    print(
        "Max side:",
        longest_side(
            agr_max_side(iter(sample))
        )
    )


    z = list(
        zip_polygons(
            islice(gen_triangle(), 5),
            islice(gen_triangle(), 5)
        )
    )

    visualize(z, "Zip polygons")
