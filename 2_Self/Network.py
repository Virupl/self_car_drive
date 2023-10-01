import random
import math
from utils import lerp


class NeuralNetwork:
    def __init__(self, neuronCounts, input_size=6, hidden_size=6, output_size=4):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weights_input_hidden = self.initialize_weights(
            input_size, hidden_size)
        self.weights_hidden_output = self.initialize_weights(
            hidden_size, output_size)
        self.biases_hidden = self.initialize_biases(hidden_size)
        self.biases_output = self.initialize_biases(output_size)

        self.levels = []
        for i in range(0, len(neuronCounts) - 1):
            self.levels.append(Level(neuronCounts[i], neuronCounts[i+1]))

    @staticmethod
    def feedForward(givenInputs, network):
        outputs = Level.feedForward(givenInputs, network.levels[0])
        for i in range(1, len(network.levels)):
            outputs = Level.feedForward(outputs, network.levels[i])

        return outputs

    @staticmethod
    def mutate(self, mutation_rate, mutation_amount=0.1):
        for i in range(self.input_size):
            for j in range(self.hidden_size):
                if random.random() < mutation_rate:
                    self.weights_input_hidden[i][j] += random.uniform(
                        -mutation_amount, mutation_amount)

        for i in range(self.hidden_size):
            for j in range(self.output_size):
                if random.random() < mutation_rate:
                    self.weights_hidden_output[i][j] += random.uniform(
                        -mutation_amount, mutation_amount)

        for i in range(self.hidden_size):
            if random.random() < mutation_rate:
                self.biases_hidden[i] += random.uniform(-mutation_amount,
                                                        mutation_amount)

        for i in range(self.output_size):
            if random.random() < mutation_rate:
                self.biases_output[i] += random.uniform(-mutation_amount,
                                                        mutation_amount)

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

    def initialize_weights(self, input_size, output_size):
        return [[random.uniform(-1, 1) for _ in range(output_size)] for _ in range(input_size)]

    def initialize_biases(self, size):
        return [random.uniform(-1, 1) for _ in range(size)]

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def forward(self, input_data):
        hidden_layer = [self.sigmoid(sum([input_data[j] * self.weights_input_hidden[i][j] for j in range(
            self.input_size)]) + self.biases_hidden[i]) for i in range(self.hidden_size)]
        output_layer = [self.sigmoid(sum([hidden_layer[j] * self.weights_hidden_output[i][j]
                                     for j in range(self.hidden_size)]) + self.biases_output[i]) for i in range(self.output_size)]
        return output_layer


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
