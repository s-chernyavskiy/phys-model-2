import math
from dataclasses import dataclass
from typing import List, Tuple

import pygame

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000
CENTER_X = WINDOW_WIDTH // 2
CENTER_Y = WINDOW_HEIGHT // 2

MATERIALS = {
    "германий": 4.1,
    "сульфид ртути 2": 3.02,
    "алмаз": 2.42,
    "стекло": 1.5,
    "вода": 1.33,
    "воздух": 1.0
}


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Ray:
    start: Point
    direction: Point
    wavelength: float
    depth: int = 0


def wavelength_to_rgb(wavelength: float, start_x: float = None) -> Tuple[int, int, int]:
    if start_x is not None and abs(start_x - (-500.0)) < 0.1:
        return 255, 255, 255

    hue = (2000.0 - wavelength) / (2000.0 - 100.0) * 0.75

    h = hue * 6.0
    sector = int(math.floor(h))
    f = h - sector
    q = 1.0 - f
    t = f

    if sector % 6 == 0:
        r, g, b = 1, t, 0
    elif sector % 6 == 1:
        r, g, b = q, 1, 0
    elif sector % 6 == 2:
        r, g, b = 0, 1, t
    elif sector % 6 == 3:
        r, g, b = 0, q, 1
    elif sector % 6 == 4:
        r, g, b = t, 0, 1
    else:
        r, g, b = 1, 0, q

    return int(r * 255), int(g * 255), int(b * 255)


class Polygon:
    def __init__(self, vertices: List[Point]):
        self.vertices = vertices


def get_regular_polygon_corners(sides: int, radius: float, center: Point) -> List[Point]:
    corners = []
    for i in range(sides):
        angle = 2 * math.pi * i / sides
        x = center.x + radius * math.cos(angle)
        y = center.y + radius * math.sin(angle)
        corners.append(Point(x, y))
    return corners


def line_intersection(p1: Point, p2: Point, p3: Point, p4: Point) -> Tuple[Point, float]:
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    x3, y3 = p3.x, p3.y
    x4, y4 = p4.x, p4.y

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denominator) < 1e-8:
        return None, 0

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
    u = (-(x1 - x2) * (y1 - y3) + (y1 - y2) * (x1 - x3)) / denominator

    if t > 1e-6 and 0 <= u <= 1:
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        return Point(x, y), t
    return None, 0


def calculate_refraction(incident: Point, normal: Point, n1: float, n2: float, wavelength: float) -> Point:
    incident = Point(incident.x / math.sqrt(incident.x ** 2 + incident.y ** 2),
                     incident.y / math.sqrt(incident.x ** 2 + incident.y ** 2))
    normal = Point(normal.x / math.sqrt(normal.x ** 2 + normal.y ** 2),
                   normal.y / math.sqrt(normal.x ** 2 + normal.y ** 2))

    dot_product = incident.x * normal.x + incident.y * normal.y
    if dot_product > 0:
        normal = Point(-normal.x, -normal.y)
        n1, n2 = n2, n1

    wavelength_factor = 1.0 + (wavelength - 1000.0) / 10000.0
    n2_adjusted = n2 * wavelength_factor

    n = n1 / n2_adjusted
    cos_i = -(incident.x * normal.x + incident.y * normal.y)
    sin_t2 = n * n * (1.0 - cos_i * cos_i)

    if sin_t2 > 1.0:
        return None

    cos_t = math.sqrt(1.0 - sin_t2)

    refracted = Point(
        n * incident.x + (n * cos_i - cos_t) * normal.x,
        n * incident.y + (n * cos_i - cos_t) * normal.y
    )

    length = math.sqrt(refracted.x ** 2 + refracted.y ** 2)
    return Point(refracted.x / length, refracted.y / length)


def draw_dashed_line(screen, start: Point, end: Point, color: Tuple[int, int, int], dash_length: float = 10.0,
                     gap_length: float = 5.0):
    dx = end.x - start.x
    dy = end.y - start.y
    distance = math.sqrt(dx * dx + dy * dy)

    if distance == 0:
        return

    dx /= distance
    dy /= distance

    current = start
    drawing = True
    remaining = distance

    while remaining > 0:
        segment_length = min(dash_length if drawing else gap_length, remaining)
        if drawing:
            next_point = Point(
                current.x + dx * segment_length,
                current.y + dy * segment_length
            )
            pygame.draw.line(screen, color,
                             (current.x + CENTER_X, current.y + CENTER_Y),
                             (next_point.x + CENTER_X, next_point.y + CENTER_Y), 2)
        current = Point(
            current.x + dx * segment_length,
            current.y + dy * segment_length
        )
        remaining -= segment_length
        drawing = not drawing


class RayTracer:
    def __init__(self, screen):
        self.screen = screen
        self.max_reflections = 20
        self.ray_length = 2000.0

    def trace_ray(self, ray: Ray, polygons: List[Polygon], material: str, environment: str, depth: int = 0):
        if depth >= self.max_reflections:
            return

        closest_intersection = None
        closest_polygon = None
        closest_normal = None
        min_t = float('inf')

        for polygon in polygons:
            for i in range(len(polygon.vertices)):
                p1 = polygon.vertices[i]
                p2 = polygon.vertices[(i + 1) % len(polygon.vertices)]

                intersection, t = line_intersection(
                    ray.start,
                    Point(ray.start.x + ray.direction.x * self.ray_length,
                          ray.start.y + ray.direction.y * self.ray_length),
                    p1, p2
                )

                if intersection and t < min_t:
                    min_t = t
                    closest_intersection = intersection
                    closest_polygon = polygon
                    dx = p2.x - p1.x
                    dy = p2.y - p1.y
                    length = math.sqrt(dx * dx + dy * dy)
                    closest_normal = Point(dy / length, -dx / length)

        if closest_intersection:
            rgb = wavelength_to_rgb(ray.wavelength, ray.start.x)
            pygame.draw.line(self.screen, rgb,
                             (ray.start.x + CENTER_X, ray.start.y + CENTER_Y),
                             (closest_intersection.x + CENTER_X, closest_intersection.y + CENTER_Y))

            n1 = MATERIALS[environment]
            n2 = MATERIALS[material]

            refracted = calculate_refraction(ray.direction, closest_normal, n1, n2, ray.wavelength)

            if refracted:
                new_ray = Ray(
                    start=closest_intersection,
                    direction=refracted,
                    wavelength=ray.wavelength,
                    depth=depth + 1
                )
                self.trace_ray_inside(closest_polygon, new_ray, polygons, material, environment)
            else:
                dot = ray.direction.x * closest_normal.x + ray.direction.y * closest_normal.y
                refl_dir = Point(
                    ray.direction.x - 2 * dot * closest_normal.x,
                    ray.direction.y - 2 * dot * closest_normal.y
                )
                new_ray = Ray(
                    start=closest_intersection,
                    direction=refl_dir,
                    wavelength=ray.wavelength,
                    depth=depth + 1
                )
                self.trace_ray(new_ray, polygons, material, environment, depth + 1)
        else:
            far_point = Point(
                ray.start.x + ray.direction.x * self.ray_length,
                ray.start.y + ray.direction.y * self.ray_length
            )
            rgb = wavelength_to_rgb(ray.wavelength, ray.start.x)
            pygame.draw.line(self.screen, rgb,
                             (ray.start.x + CENTER_X, ray.start.y + CENTER_Y),
                             (far_point.x + CENTER_X, far_point.y + CENTER_Y))

    def trace_ray_inside(self, polygon: Polygon, ray: Ray, all_polygons: List[Polygon], material: str,
                         environment: str):
        current_ray = ray
        for bounce in range(20):
            closest_intersection = None
            closest_normal = None
            min_t = float('inf')

            for i in range(len(polygon.vertices)):
                p1 = polygon.vertices[i]
                p2 = polygon.vertices[(i + 1) % len(polygon.vertices)]

                intersection, t = line_intersection(
                    current_ray.start,
                    Point(current_ray.start.x + current_ray.direction.x * self.ray_length,
                          current_ray.start.y + current_ray.direction.y * self.ray_length),
                    p1, p2
                )

                if intersection and t < min_t:
                    min_t = t
                    closest_intersection = intersection
                    dx = p2.x - p1.x
                    dy = p2.y - p1.y
                    length = math.sqrt(dx * dx + dy * dy)
                    closest_normal = Point(dy / length, -dx / length)

            if not closest_intersection:
                return

            rgb = wavelength_to_rgb(current_ray.wavelength, current_ray.start.x)
            draw_dashed_line(self.screen, current_ray.start, closest_intersection, rgb)

            n1 = MATERIALS[material]
            n2 = MATERIALS[environment]

            outward_normal = Point(-closest_normal.x, -closest_normal.y)
            refracted = calculate_refraction(current_ray.direction, outward_normal, n1, n2, current_ray.wavelength)

            if refracted:
                new_ray = Ray(
                    start=closest_intersection,
                    direction=refracted,
                    wavelength=current_ray.wavelength,
                    depth=current_ray.depth + 1
                )
                self.trace_ray(new_ray, all_polygons, material, environment, current_ray.depth + 1)
                return
            else:
                dot = current_ray.direction.x * closest_normal.x + current_ray.direction.y * closest_normal.y
                refl_dir = Point(
                    current_ray.direction.x - 2 * dot * closest_normal.x,
                    current_ray.direction.y - 2 * dot * closest_normal.y
                )
                current_ray = Ray(
                    start=closest_intersection,
                    direction=refl_dir,
                    wavelength=current_ray.wavelength,
                    depth=current_ray.depth + 1
                )

    def trace_scene(self, polygons: List[Polygon], material: str, environment: str, angle: float):
        num_rays = 7
        init_origin = Point(-500.0, 0.0)
        base_angle_rad = math.radians(angle)

        for i in range(num_rays):
            wavelength = 100.0 + (2000.0 - 100.0) * i / (num_rays - 1)
            init_dir = Point(math.cos(base_angle_rad), math.sin(base_angle_rad))
            ray = Ray(init_origin, init_dir, wavelength)
            self.trace_ray(ray, polygons, material, environment)


def rotate_point(point: Point, center: Point, angle_rad: float) -> Point:
    dx = point.x - center.x
    dy = point.y - center.y
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    new_x = center.x + dx * cos_a - dy * sin_a
    new_y = center.y + dx * sin_a + dy * cos_a
    return Point(new_x, new_y)


def get_triangle_with_angle(angle_degrees: float, radius: float, center: Point) -> List[Point]:
    angle_rad = math.radians(angle_degrees)

    height = radius * math.cos(angle_rad / 2)

    base_width = 2 * radius * math.sin(angle_rad / 2)

    top = Point(center.x, center.y - height)
    left = Point(center.x - base_width / 2, center.y + height)
    right = Point(center.x + base_width / 2, center.y + height)

    return [top, left, right]


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    base_polygons = [
        Polygon(get_regular_polygon_corners(6, 150.0, Point(0.0, 0.0))),
        Polygon(get_regular_polygon_corners(6, 120.0, Point(-400.0, -100.0))),
        Polygon(get_regular_polygon_corners(5, 140.0, Point(400.0, -80.0))),
        Polygon(get_triangle_with_angle(60.0, 200.0, Point(0.0, 0.0))),
        Polygon(get_regular_polygon_corners(4, 100.0, Point(0.0, -400.0))),
        Polygon(get_regular_polygon_corners(8, 90.0, Point(380.0, 380.0))),
        Polygon(get_regular_polygon_corners(7, 80.0, Point(-350.0, -350.0))),
        Polygon(get_regular_polygon_corners(5, 95.0, Point(350.0, -350.0))),
        Polygon(get_regular_polygon_corners(4, 85.0, Point(-320.0, 320.0))),
    ]
    ray_tracer = RayTracer(screen)

    current_material = "алмаз"
    current_environment = "воздух"
    current_angle = 0.0
    prism_angle = 60.0

    font = pygame.font.Font(None, 30)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_material = "алмаз"
                elif event.key == pygame.K_2:
                    current_material = "стекло"
                elif event.key == pygame.K_3:
                    current_material = "вода"
                elif event.key == pygame.K_4:
                    current_material = "сульфид ртути 2"
                elif event.key == pygame.K_5:
                    current_material = "германий"
                elif event.key == pygame.K_0:
                    current_material = "воздух"
                elif event.key == pygame.K_z:
                    current_environment = "воздух"
                elif event.key == pygame.K_x:
                    current_environment = "вода"
                elif event.key == pygame.K_c:
                    current_environment = "стекло"
                elif event.key == pygame.K_v:
                    current_environment = "алмаз"
                elif event.key == pygame.K_b:
                    current_environment = "сульфид ртути 2"
                elif event.key == pygame.K_n:
                    current_environment = "германий"

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            current_angle -= 2
        if keys[pygame.K_RIGHT]:
            current_angle += 2
        if keys[pygame.K_a]:
            prism_angle = max(30, prism_angle - 2)
        if keys[pygame.K_d]:
            prism_angle = min(150, prism_angle + 2)
        current_angle = current_angle % 360

        screen.fill((0, 0, 0))

        polygons = []
        for i, base_polygon in enumerate(base_polygons):
            if i == 3:
                polygons.append(Polygon(get_triangle_with_angle(prism_angle, 200.0, Point(0.0, 325.0))))
            else:
                polygons.append(base_polygon)

        for polygon in polygons:
            points = [(p.x + CENTER_X, p.y + CENTER_Y) for p in polygon.vertices]
            pygame.draw.polygon(screen, (255, 255, 255), points, 2)

        ray_tracer.trace_scene(polygons, current_material, current_environment, current_angle)

        material_text = font.render(f"Материал фигур: {current_material}", True, (255, 255, 255))
        environment_text = font.render(f"Материал среды: {current_environment}", True, (255, 255, 255))
        angle_text = font.render(f"Угол луча: {current_angle}°", True, (255, 255, 255))
        prism_text = font.render(f"Преломляющий угол призмы: {prism_angle}°", True, (255, 255, 255))

        screen.blit(material_text, (20, 20))
        screen.blit(environment_text, (WINDOW_WIDTH - 300, 20))
        screen.blit(angle_text, (20, 80))
        screen.blit(prism_text, (20, 140))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()