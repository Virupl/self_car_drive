import random
from utils import lerp


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

    @staticmethod
    def mutate(network, amount=1):
        for level in network.levels:
            for i in range(len(level.biases)):
                level.biases[i] = lerp(
                    level.biases[i], random.uniform(-1, 1), amount)
            for i in range(len(level.weights)):
                for j in range(len(level.weights[i])):
                    level.weights[i][j] = lerp(
                        level.weights[i][j], random.uniform(-1, 1), amount)


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
