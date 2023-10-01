import pygame
from utils import lerp, getRGB


class Visualizer:
    @staticmethod
    def drawNetwork(screen, network):
        margin = 50
        left = margin
        top = margin
        width = screen.get_width() - margin * 2
        height = screen.get_height() - margin * 2

        levelHeight = height / 2.26

        for i in range(len(network.levels)-1, -1, -1):
            levelTop = top - 50 + lerp((height - levelHeight), 0,
                                       (0.5 if len(network.levels) == 1 else i / (len(network.levels))))
            # ["🠉", "🠈", "🠊", "🠋"]
            # ["W", "A", "D", "S"]
            Visualizer.drawLevel(
                screen, network.levels[i], left, levelTop, width, levelHeight, ["W", "A", "D", "S"] if i == len(network.levels) - 1 else [])

    @staticmethod
    def drawLevel(screen, level, left, top, width, height, outputLabels):
        right = left + width
        bottom = top + height

        inputs = level.inputs
        outputs = level.outputs
        weights = level.weights
        biases = level.biases

        dash_length = 10

        for i in range(len(inputs)):
            for j in range(len(outputs)):
                start_x = Visualizer.get_node_x(inputs, i, left, right)
                start_y = bottom - 50
                end_x = Visualizer.get_node_x(outputs, j, left, right)
                end_y = top + 50

                # pygame.draw.line(screen, getRGB(weights[i][j]),
                #                  (start_x, start_y), (end_x, end_y), 2, dash_length)

                # Draw dashed line
                pygame.draw.line(screen, getRGB(weights[i][j]),
                                 (start_x, start_y), (end_x, end_y), 2)

        nodeRadius = 18

        for i in range(len(inputs)):
            x = Visualizer.get_node_x(inputs, i, left, right)

            # Background Black Circle
            pygame.draw.circle(screen, (0, 0, 0),
                               (int(x), int(bottom - 50)), nodeRadius, 18)

            # Outline circle
            pygame.draw.circle(screen, getRGB(biases[i-2]),
                               (int(x), int(bottom - 50)), nodeRadius*0.8, 1, True, False, True, False)

            # main circle
            pygame.draw.circle(screen, getRGB(inputs[i]),
                               (int(x), int(bottom - 50)), nodeRadius*0.6, 18)

        for i in range(len(outputs)):
            x = Visualizer.get_node_x(outputs, i, left, right)

            # Background Black Circle
            pygame.draw.circle(screen, (0, 0, 0),
                               (int(x), int(top + 50)), nodeRadius, 18)

            # Outline circle
            pygame.draw.circle(screen, getRGB(biases[i]),
                               (int(x), int(top + 50)), nodeRadius*0.8, 1)

            # main circle
            pygame.draw.circle(screen, getRGB(outputs[i]),
                               (int(x), int(top + 50)), nodeRadius*0.6, 18)

            if i < len(outputLabels) and outputLabels[i]:
                font = pygame.font.Font(None, int(nodeRadius * 1.3))
                text = font.render(outputLabels[i], True, (0, 0, 0))
                text_rect = text.get_rect(
                    center=(int(x), int(top + 50 + nodeRadius * 0.1)))
                screen.blit(text, text_rect)

    def get_node_x(nodes, index, left, right):
        return lerp(left, right, (0.5 if len(nodes) == 1 else index / (len(nodes) - 1)))
