import math
import pygame

from Sensor import Sensor
from Controls import Controls
from conf import BLUE, RED, YELLOW, BLACK, car_image
from Network import NeuralNetwork
from utils import polysIntersect


class Car:
    def __init__(self, x, y, width, height, controlType, maxSpeed=3, color=BLUE):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.color = color
        self.speed = 1
        self.acceleration = 0.2
        self.maxSpeed = maxSpeed
        self.friction = 0.05
        self.angle = 0
        self.damaged = False
        self.controlType = controlType

        self.direction = 1  # Initialize the direction as forward

        self.useBrain = controlType == "AI"

        self.controls = Controls(controlType)
        self.sensors = []

        if controlType != "DUMMY":
            # Create the sensors
            self.createSensors()
            self.brain = NeuralNetwork([len(self.sensors), 6, 4])

        self.gon2 = self.createPolygon_tCar()

    def createSensors(self):
        rayCount = 6  # Set the desired ray count for the sensors
        angle_offset = math.pi / 10  # Angle offset for spread

        # Create six sensors with a spread angle of 45 degrees
        for i in range(rayCount):
            # sensor_angle = self.angle + (i - 2.5) * angle_offset
            sensor_angle = self.angle + (i + 7.5) * angle_offset
            self.sensors.append(Sensor(self, sensor_angle, rayCount))

    def update(self, roadBorders, traffic_cars):
        if not self.damaged:
            self.move(traffic_cars)
            self.Polygon = self.createPolygon()
            self.damaged = self.assessDamage(roadBorders, traffic_cars)

        if self.sensors:
            # Update the sensors
            for sensor in self.sensors:
                sensor.update(roadBorders, traffic_cars)

            offsets = [0 if s is None else 1 -
                       s.offset for s in self.sensors]

            outputs = self.brain.feedForward(offsets, self.brain)

            if self.useBrain:
                self.controls.forward = outputs[0]
                self.controls.left = outputs[1]
                self.controls.right = outputs[2]
                self.controls.reverse = outputs[3]

    def assessDamage(self, roadBorders, traffic):
        for road_border in roadBorders:
            if polysIntersect(self.Polygon, road_border):
                return True

        for vehicle in traffic:
            if polysIntersect(self.Polygon, vehicle.gon2):
                return True

        return False

    def createPolygon(self):
        points = []
        rad = math.hypot(self.width, self.height-20)/2
        alpha = math.atan2(self.width, self.height-20)

        points.append({
            'x': self.x - math.sin(self.angle - alpha) * rad,
            'y': self.y - math.cos(self.angle - alpha) * rad
        })
        points.append({
            'x': self.x - math.sin(self.angle + alpha) * rad,
            'y': self.y - math.cos(self.angle + alpha) * rad
        })
        points.append({
            'x': self.x - math.sin(math.pi + self.angle - alpha) * rad,
            'y': self.y - math.cos(math.pi + self.angle - alpha) * rad
        })
        points.append({
            'x': self.x - math.sin(math.pi + self.angle + alpha) * rad,
            'y': self.y - math.cos(math.pi + self.angle + alpha) * rad
        })

        return points

    def createPolygon_tCar(self):
        points = []
        rad = math.hypot(self.width-15, self.height-40)/2
        alpha = math.atan2(self.width-15, self.height-40)

        points.append({
            'x': self.x - math.sin(0 - alpha) * rad,
            'y': self.y - math.cos(0 - alpha) * rad
        })
        points.append({
            'x': self.x - math.sin(0 + alpha) * rad,
            'y': self.y - math.cos(0 + alpha) * rad
        })
        points.append({
            'x': self.x - math.sin(math.pi + 0 - alpha) * rad,
            'y': self.y - math.cos(math.pi + 0 - alpha) * rad
        })
        points.append({
            'x': self.x - math.sin(math.pi + 0 + alpha) * rad,
            'y': self.y - math.cos(math.pi + 0 + alpha) * rad
        })

        return points

    def move(self, traffic_cars):
        if self.controls.forward:
            self.speed += self.acceleration
        if self.controls.reverse:
            self.speed -= self.acceleration

        if self.speed > self.maxSpeed:
            self.speed = self.maxSpeed
        if self.speed < -self.maxSpeed / 2:
            self.speed = -self.maxSpeed / 2

        if self.speed > 0:
            self.speed -= self.friction
        if self.speed < 0:
            self.speed += self.friction
        if abs(self.speed) < self.friction:
            self.speed = 0

        if self.speed != 0:
            flip = 1 if self.speed > 0 else -1
            if self.controls.left:
                self.angle += 0.03 * flip
            if self.controls.right:
                self.angle -= 0.03 * flip

        self.x -= math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

        for sensor in self.sensors:
            intersection_point1, intersection_point2 = sensor.detect(
                traffic_cars)

            if intersection_point1 or intersection_point2:
                sensor.color = RED
            else:
                sensor.color = YELLOW  # Default color

    def draw(self, screen, traffic_cars):
        if self.damaged:
            car_image.fill(BLACK)
        else:
            car_image.fill(self.color)

        x = 40
        y = 70
        d = math.sqrt(x ** 2 + y ** 2)
        angle = math.degrees(self.angle)
        scale = abs(5 * d / 400)
        rotated_image = pygame.transform.rotozoom(
            car_image, angle, scale)
        new_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, new_rect.topleft)

        # Draw the sensors
        for sensor in self.sensors:
            sensor.draw(screen, traffic_cars)
