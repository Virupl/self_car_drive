import pygame
from utils import lerp

WHITE = (255, 255, 255)


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
