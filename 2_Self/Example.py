import pygame
import math
import random
from utils import getIntersection1, getIntersection2, lerp
import numpy as np

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (150, 150, 150)


window_width = 800
screen_width = 200
networkCtx_width = 300

# Initialize Pygame
pygame.init()

height = pygame.display.Info().current_h

window = pygame.display.set_mode((window_width, height))

screen_x = (window_width - screen_width) // 5

screen = pygame.Surface((screen_width, height))

networkCtx_x = (window_width - networkCtx_width) // 1.3

networkCtx = pygame.Surface((networkCtx_width, height-70))

clock = pygame.time.Clock()

# All Class


class Road:
    def __init__(self, x, width, laneCount=3):
        self.x = x
        self.width = width
        self.laneCount = laneCount

        self.left = x - width/2
        self.right = x + width/2

        infinity = 1000000
        self.top = -infinity
        self.bottom = infinity

        topLeft = {'x': self.left, 'y': self.top}
        topRight = {'x': self.right, 'y': self.top}
        bottomLeft = {'x': self.left, 'y': self.bottom}
        bottomRight = {'x': self.right, 'y': self.bottom}
        self.borders = [
            [topLeft, bottomLeft],
            [topRight, bottomRight]
        ]

        # Define the line segments of the broken line
        self.line_segments = [
            [(self.left, -infinity), (self.left, infinity)],
            [(self.right, -infinity), (self.right, infinity)]
        ]

    def getLaneCenter(self, laneIndex):
        laneWidth = self.width / self.laneCount
        return self.left + laneWidth/2 + min(laneIndex, self.laneCount-1) * laneWidth

    def draw(self, screen, car):
        # Calculate the road speed based on car's speed and direction
        road_speed = car.speed * car.direction
        self.top += road_speed  # Update the top coordinate of the road
        self.bottom += road_speed  # Update the bottom coordinate of the road

        for i in range(1, self.laneCount):
            x = lerp(self.left, self.right, i / self.laneCount)
            dash_length = 40  # Length of each dash
            gap_length = 40  # Length of the gap between dashes
            num_dashes = int((self.bottom - self.top) /
                             (dash_length + gap_length))

            for j in range(num_dashes):
                start_y = self.top + j * (dash_length + gap_length)
                end_y = start_y + dash_length

                if (car.speed * car.direction >= 0):
                    # Car moving forward, road moves backward
                    start_y += car.speed
                    end_y += car.speed
                else:
                    # Car moving backward, road moves forward
                    start_y -= car.speed
                    end_y -= car.speed
                pygame.draw.line(screen, WHITE, (x, start_y), (x, end_y), 5)

        for border in self.borders:
            pygame.draw.line(
                screen, WHITE, (border[0]['x'], border[0]['y']), (border[1]['x'], border[1]['y']), 5)

#######################################


class Sensor:
    def __init__(self, car, sensor_angle, rayCount):
        self.raySpread = math.pi / 2
        self.rayCount = rayCount
        self.rayLength = 100
        self.car = car
        self.angle = sensor_angle
        self.offset = 0
        self.color = RED

        self.detected_color = RED

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
            poly = traffic[i].polygon
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

    def calculateOffset(self, ray, touch):
        # Implement the offset calculation logic based on your specific criteria
        # You can access the necessary values from the 'ray' and 'touch' dictionaries
        # and perform the calculations to determine the offset
        # Return the calculated offset value

        # Example offset calculation
        distance = touch['distance']
        return distance

    def castRays(self):
        self.rays = []

        for i in range(self.rayCount):
            rayAngle = lerp(
                self.raySpread / 2,
                -self.raySpread / 2,
                0.5 if self.rayCount == 1 else i / (self.rayCount - 1)
            ) + self.car.angle

            start = {'x': self.car.X, 'y': self.car.Y}
            end = {
                'x': self.car.X - math.sin(rayAngle) * self.rayLength,
                'y': self.car.Y - math.cos(rayAngle) * self.rayLength
            }
            self.rays.append([start, end])

    def detect_border(self):
        x = self.car.X + self.offset * math.sin(self.angle)
        y = self.car.X + self.offset * math.cos(self.angle)
        end_x = x + self.rayLength * math.sin(self.car.angle + self.angle)
        end_y = y + self.rayLength * math.cos(self.car.angle + self.angle)

        start_point = {'x': x, 'y': y}
        end_point = {'x': end_x, 'y': end_y}

        intersection_point1 = None
        closest_distance = float('inf')

        for border in road.borders:
            border_start = {'x': border[0]['x'], 'y': border[0]['y']}
            border_end = {'x': border[1]['x'], 'y': border[1]['y']}

            point1 = getIntersection1(
                start_point, end_point, border_start, border_end)
            if point1:
                distance = math.sqrt(
                    (start_point['x'] - point1['x']) ** 2 + (start_point['y'] - point1['y']) ** 2)
                if distance < closest_distance:
                    closest_distance = distance
                    intersection_point1 = point1

        return intersection_point1

    def detect_car(self):
        x = self.car.X + self.offset * math.sin(self.angle)
        y = self.car.Y + self.offset * math.cos(self.angle)
        end_x = x + self.rayLength * math.sin(self.car.angle + self.angle)
        end_y = y + self.rayLength * math.cos(self.car.angle + self.angle)

        start_point = (x, y)
        end_point = (end_x, end_y)

        intersection_point2 = None
        closest_distance = float('inf')

        for t_car in traffic_cars:
            car_rect = pygame.Rect(t_car.x, t_car.y, t_car.width, t_car.height)

            point2 = getIntersection2(
                start_point, end_point, car_rect.bottomleft, car_rect.bottomright)
            if point2:
                distance = math.sqrt(
                    (start_point[0] - point2[0])**2 + (start_point[1] - point2[1])**2)
                if distance <= closest_distance:
                    closest_distance = distance
                    intersection_point2 = point2
                    detected_car = t_car
                    detected_cars.append(detected_car)

        return intersection_point2

    def draw(self, screen):
        x = self.car.X + self.offset * math.sin(self.angle)
        y = self.car.Y + self.offset * math.cos(self.angle)
        end_x = x + self.rayLength * math.sin(self.car.angle + self.angle)
        end_y = y + self.rayLength * math.cos(self.car.angle + self.angle)

        color = self.color  # Default color
        intersection_point1 = self.detect_border()
        if intersection_point1:
            color = self.detected_color  # Detected color
        else:
            color = self.color  # Default color

        pygame.draw.line(screen, color, (x, y), (end_x, end_y), 2)
        # pygame.draw.line(screen, self.color, (x, y), (end_x, end_y), 2)

###############################################


class Car:
    def __init__(self, x, y, width, height, controlType):
        self.X = x
        self.Y = y
        self.width = width
        self.height = height

        self.speed = 1
        self.acceleration = 0.2
        self.maxSpeed = 3
        self.friction = 0.05
        self.angle = 0

        self.direction = 1  # Initialize the direction as forward

        self.useBrain = controlType == "AI"

        self.controls = Controls()

        self.sensors = []

        # Create the sensors
        self.createSensors()

        if controlType != "DUMMY":
            self.brain = NeuralNetwork([len(self.sensors), 6, 4])

    def createSensors(self):
        rayCount = 6  # Set the desired ray count for the sensors
        angle_offset = math.pi / 10  # Angle offset for spread

        # Create six sensors with a spread angle of 45 degrees
        for i in range(rayCount):
            sensor_angle = self.angle + (i + 7.5) * angle_offset
            self.sensors.append(Sensor(self, sensor_angle, rayCount))

    def update(self, traffic_cars):
        self.move()

        if self.sensors:
            # Update the sensors
            for sensor in self.sensors:
                sensor.update(road.borders, traffic_cars)

            offsets = [0 if s is None else 1 -
                       s.offset for s in self.sensors]

            outputs = self.brain.feedForward(offsets, self.brain)

            if self.useBrain:
                self.controls.forward = outputs[0]
                self.controls.left = outputs[1]
                self.controls.right = outputs[2]
                self.controls.reverse = outputs[3]

    def move(self):
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

        new_x = self.X - math.sin(self.angle) * self.speed
        new_y = self.Y - math.cos(self.angle) * self.speed

        # Check if the new position is within the road boundaries
        if road.left <= new_x <= road.right:
            self.X = new_x
        if road.top <= new_y <= road.bottom:
            self.Y = new_y

        # Check for collision with road borders
        if new_x - self.width / 2 < road.left or new_x + self.width / 2 > road.right:
            car_image.fill(BLACK, special_flags=pygame.BLEND_MULT)
            self.speed = 0
            exit()
        elif new_y - self.height / 2 < road.top or new_y + self.height / 2 > road.bottom:
            car_image.fill(BLACK, special_flags=pygame.BLEND_MULT)
            self.speed = 0
            exit()

        for t_car in traffic_cars:
            if (
                pygame.Rect(self.X, self.Y, self.width, self.height).colliderect(pygame.Rect(t_car.x, t_car.y, t_car.width, t_car.height)) or
                pygame.Rect(self.X, self.Y, self.width, self.height).colliderect(pygame.Rect(t_car.x + t_car.width, t_car.y, 1, t_car.height)) or
                pygame.Rect(self.X, self.Y, self.width, self.height).colliderect(pygame.Rect(t_car.x, t_car.y + t_car.height, t_car.width, 1)) or
                pygame.Rect(self.X, self.Y, self.width, self.height).colliderect(pygame.Rect(t_car.x, t_car.y, t_car.width, 1)) or
                pygame.Rect(self.X, self.Y, self.width, self.height).colliderect(
                    pygame.Rect(t_car.x, t_car.y, 1, t_car.height))
            ):
                car_image.fill(BLACK, special_flags=pygame.BLEND_MULT)
                self.speed = 0  # Stop the car's speed
                exit()

        for sensor in self.sensors:
            intersection_point1 = sensor.detect_border()
            intersection_point2 = sensor.detect_car()
            if intersection_point1 or intersection_point2:
                sensor.color = RED
                for cars in detected_cars:
                    pass
                    # print("Detected car:", cars)
            else:
                sensor.color = YELLOW

        # for i in range(0, len(self.sensors)):
        #     if self.sensors[i].color == RED:
        #         print(self.sensors[i])

    def draw(self, screen):
        x = 40
        y = 70
        d = math.sqrt(x ** 2 + y ** 2)
        angle = math.degrees(self.angle)
        scale = abs(5 * d / 400)
        rotated_image = pygame.transform.rotozoom(
            car_image, angle, scale)
        new_rect = rotated_image.get_rect(center=(self.X, self.Y))
        screen.blit(rotated_image, new_rect.topleft)

        # Draw the sensors
        for sensor in self.sensors:
            sensor.draw(screen)


##########################################################


class Traffic_car:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.angle = 0

        self.speed = 2

        self.polygon = self.createPolygon()

    def update(self):
        self.y += self.speed

    def createPolygon(self):
        points = []
        rad = math.hypot(self.width, self.height) / 2
        alpha = math.atan2(self.width, self.height)
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

    def draw(self, screen):
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.height))

#########################################################################


class Controls:
    def __init__(self):
        self.forward = False
        self.left = False
        self.right = False
        self.reverse = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.left = True
            elif event.key == pygame.K_RIGHT:
                self.right = True
            elif event.key == pygame.K_UP:
                self.forward = True
            elif event.key == pygame.K_DOWN:
                self.reverse = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.left = False
            elif event.key == pygame.K_RIGHT:
                self.right = False
            elif event.key == pygame.K_UP:
                self.forward = False
            elif event.key == pygame.K_DOWN:
                self.reverse = False

#############################################################


class NeuralNetwork:
    def __init__(self, neuronCounts):
        self.levels = []
        for i in range(0, len(neuronCounts) - 1):
            self.levels.append(Level(neuronCounts[i], neuronCounts[i+1]))

    @staticmethod
    def feedForward(givenInputs, network):
        outputs = Level.feedForward(givenInputs, network.levels[0])
        for i in range(1, len(network.levels)):
            outputs = Level.feedForward(outputs, network.levels[i])
        return outputs

    # @staticmethod
    # def mutate(network, amount=1):
    #     for level in network.levels:
    #         for i in range(len(level.biases)):
    #             level.biases[i] = lerp(
    #                 level.biases[i], random.uniform(-1, 1), amount)
    #         for i in range(len(level.weights)):
    #             for j in range(len(level.weights[i])):
    #                 level.weights[i][j] = lerp(
    #                     level.weights[i][j], random.uniform(-1, 1), amount)


class Level:
    def __init__(self, inputCount, outputCount):
        self.inputs = [None] * inputCount
        self.outputs = [None] * outputCount
        self.biases = [None] * outputCount
        self.weights = [[None] * outputCount for _ in range(inputCount)]
        self.randomize()

    def randomize(self):
        for i in range(len(self.inputs)):
            for j in range(len(self.outputs)):
                self.weights[i][j] = random.uniform(-1, 1)
        for i in range(len(self.biases)):
            self.biases[i] = random.uniform(-1, 1)

    @staticmethod
    def feedForward(givenInputs, level):
        for i in range(len(level.inputs)):
            level.inputs[i] = givenInputs[i]
        for i in range(len(level.outputs)):
            sum = 0
            for j in range(len(level.inputs)):
                sum += level.inputs[j] * level.weights[j][i]
            if sum > level.biases[i]:
                level.outputs[i] = 1
            else:
                level.outputs[i] = 0
        return level.outputs

####################################################################


visu_angle = 0  # Initial angle


class Visualizer:
    @staticmethod
    def drawNetwork(ctx, network):
        margin = 50
        left = margin
        top = margin
        width = ctx.get_width() - margin * 2
        height = ctx.get_height() - margin * 2

        levelHeight = height / len(network.levels)

        for i in range(len(network.levels)-1, -1, -1):
            # levelTop = top + 30 + ((height - levelHeight) *
            #                      (1 if len(network.levels) == 1 else i / (len(network.levels))))

            # ["🠉", "🠈", "🠊", "🠋"]
            # ["W", "A", "D", "S"]
            levelTop = top - 130 + lerp((height - levelHeight), 0,
                                        (1 if len(network.levels) == 1 else i / (len(network.levels))))
            Visualizer.drawLevel(ctx, network.levels[i], left, levelTop, width, levelHeight,
                                 ["W", "A", "D", "S"] if i == len(network.levels) - 1 else [])

    @staticmethod
    def drawLevel(ctx, level, left, top, width, height, outputLabels):
        right = left + width
        bottom = top + height

        inputs = level.inputs
        outputs = level.outputs
        weights = level.weights
        biases = level.biases

        nodeRadius = 18

        # Draw connections between nodes
        for i in range(len(inputs)):
            for j in range(len(outputs)):
                start_x = Visualizer.get_node_x(inputs, i, left, right)
                start_y = bottom
                end_x = Visualizer.get_node_x(outputs, j, left, right)
                end_y = top

                pygame.draw.line(ctx, (255, 255, 255),
                                 (start_x, start_y), (end_x, end_y), 2)

        # Draw input nodes
        for i in range(len(inputs)):
            x = Visualizer.get_node_x(inputs, i, left, right)

            pygame.draw.circle(
                ctx, (0, 255, 0), (int(x), int(bottom)), nodeRadius-4, 2)

            # # Call the rotate_circle function
            # Visualizer.rotate_circle(ctx, width, height, int(x), int(bottom))

            # Input YELLOW Circle
            if inputs[i] == 0:
                pygame.draw.circle(ctx, (59, 45, 6), (int(
                    x), int(bottom)), int(nodeRadius * 0.6))
            else:
                pygame.draw.circle(ctx, Visualizer.get_rgba(
                    inputs[i]), (int(x), int(bottom)), int(nodeRadius * 1))

        # Draw output nodes
        for i in range(len(outputs)):
            x = Visualizer.get_node_x(outputs, i, left, right)

            pygame.draw.circle(
                ctx, (0, 0, 255), (int(x), int(top)), nodeRadius, 2)

            # Call the rotate_circle function
            # Visualizer.rotate_circle(ctx, width, height, int(x), int(top))

            # For RED Circle
            # pygame.draw.circle(ctx, Visualizer.get_rgba(biases[i]), (int(
            #     x), int(top)), int(nodeRadius * 0.9))

            #  First Up Circle YELLOW
            if outputs[i] == 0:
                pygame.draw.circle(ctx, (59, 45, 6), (int(
                    x), int(top)), int(nodeRadius * 0.6))
            else:
                pygame.draw.circle(ctx, Visualizer.get_rgba(outputs[i]), (int(
                    x), int(top)), int(nodeRadius * 0.6))

            if i < len(outputLabels) and outputLabels[i]:
                font = pygame.font.Font(None, int(nodeRadius * 1.5))
                text = font.render(outputLabels[i], True, (0, 0, 0))
                text_rect = text.get_rect(
                    center=(int(x), int(top + nodeRadius * 0.1)))
                ctx.blit(text, text_rect)

    # def get_node_x(nodes, index, left, right):
    #     return left + ((right - left) * (0.5 if len(nodes) == 1 else index / (len(nodes) - 1)))

    def get_node_x(nodes, index, left, right):
        return lerp(left, right, (0.5 if len(nodes) == 1 else index / (len(nodes) - 1)))

    def get_rgba(value):
        if value == None:
            value = 0
        if value >= 0:
            return 255, 255, 0
        else:
            return 255, 0, 0

    def rotate_circle(ctx, width, height, x, y):
        global visu_angle

        # Define circle parameters
        center_x, center_y = width // 2, height // 2
        radius = 300
        num_objects = 12  # Number of objects to rotate around the circle
        object_radius = 12

        # Set colors
        background_color = (255, 0, 0, 255)  # RGBA values
        object_color = (0, 0, 0)

        # Calculate the angle increment based on the number of objects
        angle_increment = 360 / num_objects

        # Rotate and draw the objects around the circle
        for i in range(num_objects):
            # Calculate the position of each object
            object_angle = math.radians(visu_angle + i * angle_increment)
            object_x = int(center_x + radius * math.cos(object_angle))
            object_y = int(center_y + radius * math.sin(object_angle))

            # Create a surface for the object and rotate it
            object_surface = pygame.Surface(
                (object_radius * 2, object_radius * 2))

            object_surface = object_surface.convert_alpha()

            # Fill with background color for transparency
            object_surface.fill(background_color)

            pygame.draw.circle(object_surface, object_color,
                               (object_radius, object_radius), object_radius)

            rotated_surface = pygame.transform.rotate(
                object_surface, visu_angle + i * angle_increment)

            # Get the rect of the rotated object surface and set its position
            rotated_rect = rotated_surface.get_rect(
                center=(x, y))

            # Draw the rotated object
            ctx.blit(rotated_surface, rotated_rect)

            # Increment the angle for rotation
            visu_angle += 1


#########################################################################
# Road Initialized
road = Road(screen_width / 2, screen_width * 0.9)

# Load car image
car_image = pygame.image.load("car1.png")

# if LANE_INDEX = 0 Car Left side
# if LANE_INDEX = 0.5 Car Middel
# if LANE_INDEX = 1 Car Right side
LANE_INDEX = 0.5
car_ori_height = car_image.get_height()
car = Car(road.getLaneCenter(LANE_INDEX),
          height - 100 - car_ori_height, 40, 70, "AI")


pygame.Surface.convert_alpha(car_image)
car_image.set_colorkey((0, 0, 0))

# Traffic Cars Call
traffic_cars = [
    # 0.3 = 0
    # 0.75 = 1
    # 1.75 = 2
    # Traffic_car(road.getLaneCenter(0.75), 500, 30, 50, RED),
    Traffic_car(road.getLaneCenter(-0.3), 0, 30, 50, RED),
    Traffic_car(road.getLaneCenter(0.75), -130, 30, 50, RED),
    Traffic_car(road.getLaneCenter(1.75), -260, 30, 50, RED),
    Traffic_car(road.getLaneCenter(1.75), -390, 30, 50, RED),
    Traffic_car(road.getLaneCenter(0.75), -520, 30, 50, RED),
    Traffic_car(road.getLaneCenter(-0.3), -650, 30, 50, RED),
    Traffic_car(road.getLaneCenter(-0.3), -780, 30, 50, RED),
    Traffic_car(road.getLaneCenter(0.75), -910, 30, 50, RED),
    Traffic_car(road.getLaneCenter(1.75), -1040, 30, 50, RED),
]

# Detected Cars
detected_cars = []


def animate():
    car.update(traffic_cars)

    for t_car in traffic_cars:
        t_car.update()

    window.fill(WHITE)
    screen.fill(GRAY)
    networkCtx.fill(BLACK)

    road.draw(screen, car)
    car.draw(screen)

    for t_car in traffic_cars:
        t_car.draw(screen)

    # for cars in detected_cars:
    #     if cars:
    #         pygame.draw.rect(screen, BLUE,
    #                          (cars.x, cars.y, cars.width, cars.height))
    #         cars.speed = 0

    Visualizer.drawNetwork(networkCtx, car.brain)

    # Blit the Screen on the Window
    window.blit(screen, (screen_x, 0))
    window.blit(networkCtx, (networkCtx_x, 0))

    pygame.display.flip()


if __name__ == '__main__':
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                car.controls.handle_event(event)

        animate()

        clock.tick(60)

    # Quit the game
    pygame.quit()
