# import pickle

# # Data to be stored
# my_data = {
#     'name': 'John Doe',
#     'age': 30,
#     'email': 'johndoe@example.com'
# }

# # Save data to a file using pickle
# with open('data.pickle', 'wb') as f:
#     pickle.dump(my_data, f)

# # Load data from the file
# with open('data.pickle', 'rb') as f:
#     loaded_data = pickle.load(f)

# # Access the loaded data
# print(loaded_data)


# import pickle

# # Load the "bestBrain" data from the "data.pickle" file
# with open('data.pickle', 'rb') as f:
#     best_brain = pickle.load(f)

# # Iterate over cars and assign the loaded brain data
# for i in range(len(cars)):
#     cars[i].brain = best_brain

#     if i != 0:
#         NeuralNetwork.mutate(cars[i].brain, 0.1)


# import pygame
# import math

# # Initialize Pygame
# pygame.init()

# # Set up the display
# width, height = 800, 600
# screen = pygame.display.set_mode((width, height))
# pygame.display.set_caption("Dotted Circle")

# # Define circle parameters
# center_x, center_y = width // 2, height // 2
# radius = 100
# dot_radius = 2
# dot_gap = 4  # Distance between two dots

# # Set colors
# background_color = (255, 255, 255)
# dot_color = (0, 0, 0)

# # Main loop
# running = True
# while running:
#     # Handle events
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Clear the screen
#     screen.fill(background_color)

#     # Draw the dotted circle
#     for angle in range(0, 360, dot_gap):
#         # Calculate the position of each dot
#         radian = math.radians(angle)
#         dot_x = int(center_x + radius * math.cos(radian))
#         dot_y = int(center_y + radius * math.sin(radian))

#         # Draw the dot
#         pygame.draw.circle(screen, dot_color, (dot_x, dot_y), dot_radius)

#     # Update the display
#     pygame.display.flip()

# # Quit the program
# pygame.quit()


# import pygame
# import math

# # Initialize Pygame
# pygame.init()

# # Set up the display
# width, height = 800, 600
# screen = pygame.display.set_mode((width, height))
# pygame.display.set_caption("Rotating Objects around a Circle")

# # Define circle parameters
# center_x, center_y = width // 2, height // 2
# radius = 20
# num_objects = 10  # Number of objects to rotate around the circle
# object_radius = 2

# # Set colors
# background_color = (255, 255, 255)
# object_color = (0, 0, 0)


# running = True
# angle = 0  # Initial


# while running:
#     # Handle events
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Clear the screen
#     screen.fill(background_color)

#     # Calculate the angle increment based on the number of objects
#     angle_increment = 360 / num_objects

#     # Rotate and draw the objects around the circle
#     for i in range(num_objects):
#         # Calculate the position of each object
#         object_angle = math.radians(angle + i * angle_increment)
#         object_x = int(center_x + radius * math.cos(object_angle))
#         object_y = int(center_y + radius * math.sin(object_angle))

#         # Create a surface for the object and rotate it
#         object_surface = pygame.Surface((object_radius * 2, object_radius * 2))

#         # Fill with background color for transparency
#         object_surface.fill(background_color)

#         pygame.draw.circle(object_surface, object_color,
#                            (object_radius, object_radius), object_radius)

#         rotated_surface = pygame.transform.rotate(
#             object_surface, angle + i * angle_increment)

#         # Get the rect of the rotated object surface and set its position
#         rotated_rect = rotated_surface.get_rect(
#             center=(object_x, object_y))

#         # Draw the rotated object
#         screen.blit(rotated_surface, rotated_rect)

#     # Update the display
#     pygame.display.flip()

#     # Increment the angle for rotation
#     angle += 1

# # Quit the program
# pygame.quit()


# import pygame

# # Initialize Pygame
# pygame.init()

# # Set up the screen
# screen_width = 800
# screen_height = 600
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("Rectangle Color Example")

# # Define the color with RGBA values
# red = 255
# green = 0
# blue = 0
# alpha = 0  # 0 (transparent) to 255 (opaque)
# # RGBA values (Red: 255, Green: 0, Blue: 0, Alpha: 128)
# color = (red, green, blue, alpha)

# # Create a rectangle
# rect_width = 200
# rect_height = 100
# rect_x = (screen_width - rect_width) // 2
# rect_y = (screen_height - rect_height) // 2
# rectangle = pygame.Rect(rect_x, rect_y, rect_width, rect_height)

# # Main game loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Fill the screen with white color
#     screen.fill((255, 255, 255))

#     # Draw the rectangle with the specified color
#     pygame.draw.rect(screen, color, rectangle)

#     # Update the screen
#     pygame.display.flip()

# # Quit the game
# pygame.quit()


# import pygame

# # Initialize Pygame
# pygame.init()

# # Set up the screen
# screen_width = 800
# screen_height = 600
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("Transparent Rectangle Example")

# # Create a transparent surface
# transparent_surface = pygame.Surface((200, 100), pygame.SRCALPHA)
# alpha_value = 12  # 0 (transparent) to 255 (opaque)
# # RGBA values (Red: 255, Green: 0, Blue: 0, Alpha: 128)
# transparent_surface.fill((255, 0, 0, alpha_value))

# # Create a rectangle
# rect_x = (screen_width - transparent_surface.get_width()) // 2
# rect_y = (screen_height - transparent_surface.get_height()) // 2
# rectangle = pygame.Rect(
#     rect_x, rect_y, transparent_surface.get_width(), transparent_surface.get_height())

# # Main game loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Fill the screen with white color
#     screen.fill((255, 255, 255))

#     # Draw the transparent surface onto the screen
#     screen.blit(transparent_surface, (rect_x, rect_y))

#     # Update the screen
#     pygame.display.flip()

# # Quit the game
# pygame.quit()


import pygame

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Transparent Circle Example")

# Create a transparent surface
transparent_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
alpha_value = 128  # 0 (transparent) to 255 (opaque)
# RGBA values (Red: 255, Green: 0, Blue: 0, Alpha: 128)
color = (255, 0, 0, alpha_value)
pygame.draw.circle(transparent_surface, color, (100, 100), 80, 5)

# Create a rectangle
rect_x = (screen_width - transparent_surface.get_width()) // 2
rect_y = (screen_height - transparent_surface.get_height()) // 2
rectangle = pygame.Rect(
    rect_x, rect_y, transparent_surface.get_width(), transparent_surface.get_height())

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white color
    screen.fill((255, 255, 255))

    # Draw the transparent surface onto the screen
    screen.blit(transparent_surface, (rect_x, rect_y))

    # Update the screen
    pygame.display.flip()

# Quit the game
pygame.quit()
