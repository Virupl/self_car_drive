import pygame
import math

from utils import getIntersection1, getIntersection2, lerp
from conf import RED, BLACK, YELLOW, road, detected_cars


class Sensor:
    def __init__(self, car, sensor_angle, rayCount):
        self.raySpread = math.pi / 2
        self.rayCount = rayCount
        self.rayLength = 120
        self.car = car
        self.angle = sensor_angle
        self.offset = 0
        self.color = YELLOW
        self.rays = []

        self.detected_color = BLACK

    def update(self, roadBorders, traffic):
        self.castRays()
        self.readings = []
        for i in range(len(self.rays)):
            self.readings.append(
                self.getReading(
                    self.rays[i],
                    roadBorders,
                    traffic
                )
            )

    def getIntersection(self, A, B, C, D):
        tTop = (D['x'] - C['x']) * (A['y'] - C['y']) - \
            (D['y'] - C['y']) * (A['x'] - C['x'])
        uTop = (C['y'] - A['y']) * (A['x'] - B['x']) - \
            (C['x'] - A['x']) * (A['y'] - B['y'])
        bottom = (D['y'] - C['y']) * (B['x'] - A['x']) - \
            (D['x'] - C['x']) * (B['y'] - A['y'])

        if bottom != 0:
            t = tTop / bottom
            u = uTop / bottom
            if 0 <= t <= 1 and 0 <= u <= 1:
                return {
                    'x': self.lerp(A['x'], B['x'], t),
                    'y': self.lerp(A['y'], B['y'], t),
                    'distance': t  # Assuming 't' represents the distance
                }

        return None

    def lerp(self, start, end, t):
        return start + (end - start) * t

    def getReading(self, ray, roadBorders, traffic):
        touches = []

        for i in range(len(roadBorders)):
            touch = self.getIntersection(
                ray[0],
                ray[1],
                roadBorders[i][0],
                roadBorders[i][1]
            )
            if touch:
                touch['offset'] = touch['distance']
                touches.append(touch)

        for i in range(len(traffic)):
            poly = traffic[i].gon2
            for j in range(len(poly)):
                value = self.getIntersection(
                    ray[0],
                    ray[1],
                    poly[j],
                    poly[(j + 1) % len(poly)]
                )
                if value:
                    value['offset'] = value['distance']
                    touches.append(value)

        if len(touches) == 0:
            return None
        else:
            offsets = [e['offset'] for e in touches]
            minOffset = min(offsets)
            return next((e for e in touches if e['offset'] == minOffset), None)

    def castRays(self):
        self.rays = []  # Clear existing rays
        for i in range(self.rayCount):
            rayAngle = lerp(
                self.raySpread / 2,
                -self.raySpread / 2,
                0.5 if self.rayCount == 1 else i / (self.rayCount - 1)
            ) + self.car.angle

            start = {
                'x': self.car.x + self.offset * math.sin(self.car.angle),
                'y': self.car.y + self.offset * math.cos(self.car.angle)
            }
            end = {
                'x': start['x'] - math.sin(rayAngle) * self.rayLength,
                'y': start['y'] - math.cos(rayAngle) * self.rayLength
            }

            self.rays.append([start, end])

    def detect(self, traffic_cars):
        x = self.car.x + self.offset * math.sin(self.car.angle)
        y = self.car.y + self.offset * math.cos(self.car.angle)
        end_x = x + self.rayLength * math.sin(self.car.angle + self.angle)
        end_y = y + self.rayLength * math.cos(self.car.angle + self.angle)

        start_point_border = {'x': x, 'y': y}
        end_point_border = {'x': end_x, 'y': end_y}

        start_point_t_car = (x, y)
        end_point = (end_x, end_y)

        intersection_point1 = None
        intersection_point2 = None
        closest_distance = float('inf')

        for border in road.borders:
            border_start = {'x': border[0]['x'], 'y': border[0]['y']}
            border_end = {'x': border[1]['x'], 'y': border[1]['y']}

            point1 = getIntersection1(
                start_point_border, end_point_border, border_start, border_end)
            if point1:
                distance = math.sqrt(
                    (start_point_border['x'] - point1['x']) ** 2 + (start_point_border['y'] - point1['y']) ** 2)
                if distance < closest_distance:
                    closest_distance = distance
                    intersection_point1 = point1

        for t_car in traffic_cars:
            car_rect = pygame.Rect(t_car.x, t_car.y, t_car.width, t_car.height)

            point2 = getIntersection2(
                start_point_t_car, end_point, car_rect.bottomleft, car_rect.bottomright)
            if point2:
                distance = math.sqrt(
                    (start_point_t_car[0] - point2[0])**2 + (start_point_t_car[1] - point2[1])**2)
                if distance <= closest_distance:
                    closest_distance = distance
                    intersection_point2 = point2
                    detected_car = t_car
                    detected_cars.append(detected_car)

        return intersection_point1, intersection_point2

    def draw(self, screen, traffic_cars):
        color = self.color  # Default color

        intersection_point1, intersection_point2 = self.detect(traffic_cars)

        if intersection_point1 or intersection_point2:
            color = self.detected_color  # Detected color
        else:
            color = self.color  # Default color

        for i in range(self.rayCount):
            start_x = self.rays[i][0]['x']
            start_y = self.rays[i][0]['y']

            end = self.rays[i][1]

            if self.readings[i]:
                end = self.readings[i]

            pygame.draw.line(screen, YELLOW, (start_x, start_y),
                             (end['x'], end['y']), 2)

            pygame.draw.line(
                screen, BLACK, (self.rays[i][1]['x'], self.rays[i][1]['y']), (end['x'], end['y']), 2)
