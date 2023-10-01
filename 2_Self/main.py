import pygame
import pickle
import os
from pathlib import Path

from Car import Car, car_image
from conf import window_width, screen_width, networkCtx_width, road, WHITE, GRAY, RED, BLACK
from Visualizer import Visualizer
from Network import NeuralNetwork
from Button import Button


# Initialize Pygame
pygame.init()

font = pygame.font.SysFont("Arial", 5)

height = pygame.display.Info().current_h
window = pygame.display.set_mode((window_width, height))
screen_x = (window_width - screen_width) // 5
screen = pygame.Surface((screen_width, height))
networkCtx_x = (window_width - networkCtx_width) // 1.3
networkCtx = pygame.Surface((networkCtx_width, height-70))
clock = pygame.time.Clock()

# if LANE_INDEX = 0 Car Left side
# if LANE_INDEX = 1 Car Middel
# if LANE_INDEX = 2 Car Right side
LANE_INDEX = 1
car_ori_height = car_image.get_height()


def generateCars(N):
    cars = []
    for _ in range(0, N):
        cars.append(Car(road.getLaneCenter(LANE_INDEX),
                    height - 100 - car_ori_height, 40, 70, "AI"))

    return cars


N = 100
cars = generateCars(N)

pygame.Surface.convert_alpha(car_image)
car_image.set_colorkey((0, 0, 0))

traffic_cars = [
    Car(road.getLaneCenter(0), 500, 40, 70, "DUMMY", 3, RED),
    Car(road.getLaneCenter(1), 250, 40, 70, "DUMMY", 3, RED),
    Car(road.getLaneCenter(3), 400, 40, 70, "DUMMY", 3, RED),
    Car(road.getLaneCenter(0), 400, 40, 70, "DUMMY", 3, RED),
]

bestCar = cars[0]

# Create a Save button instance
save_button = Button((335, 300, 40, 40),
                     "./2_Self/Save-Button.jpg", lambda: save_data())

# Create a Delete button instance
delete_button = Button((335, 400, 40, 40),
                       "./2_Self/Delete-Button.jpg", lambda: delete_data())


def save_data():
    print("save")
    data = {'BestBrain': bestCar.brain}
    file_path = './2_Self/data.pickle'
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)
    file.close()


def delete_data():
    print("delete")
    file_path = './2_Self/data.pickle'  # Specify the file path of the pickle files

    # Check if the pickle file exists
    if os.path.exists(file_path):
        # Delete the pickle file
        os.remove(file_path)
        print("Data file deleted successfully.")
    else:
        print("Data file does not exist.")


def read_data():
    file_path = Path('./2_Self/data.pickle')
    file_path.touch(exist_ok=True)

    try:
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
        for i in range(0, len(cars)):
            bestCar.brain = data['BestBrain']

            if i != 0:
                NeuralNetwork.mutate(bestCar.brain, 0.1)

    except EOFError:
        if EOFError:
            save_data()

    file.close()


read_data()


def animate():
    global bestCar
    for car in cars:
        car.update(road.borders, traffic_cars)

    for t in traffic_cars:
        t.update(road.borders, [])

    window.fill(WHITE)
    screen.fill(GRAY)
    networkCtx.fill(BLACK)

    road.draw(screen, car)

    for car in cars:
        car.draw(screen, traffic_cars)

    bestCar = min(cars, key=lambda c: c.y)

    bestCar.draw(screen, traffic_cars, True)

    for t in traffic_cars:
        t.draw(screen, [])

    save_button.draw(window)
    delete_button.draw(window)

    Visualizer.drawNetwork(networkCtx, bestCar.brain)

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
                match bestCar.controls.type:
                    case "AI":
                        bestCar.controls.handle_event(event)
                    case "DUMMY":
                        cars[0].controls.forward = True
                        # self.speed = 3

                save_button.handle_event(event)
                delete_button.handle_event(event)

        animate()

        clock.tick(60)

    # Quit the game
    pygame.quit()
