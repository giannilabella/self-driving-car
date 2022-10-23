import numpy as np
import numpy.typing as npt

from utils import sigmoid
from _types import ControlOutput

class NeuralNetwork :
    def __init__(self, neuron_counts: list[int]) -> None:
        self.__levels: list[Level] = []

        for index, neuron_count in enumerate(neuron_counts[:-1]) :
            is_hidden = True if index + 1 != len(neuron_counts) - 1 else False

            self.__levels.append(
                Level(
                    neuron_count,
                    neuron_counts[index + 1],
                    is_hidden
                )
            )

    @property
    def levels (self) :
        return self.__levels

    @staticmethod
    def feed_forward (given_inputs: list[float], network: 'NeuralNetwork') -> ControlOutput :
        # Put given inputs to outputs vector
        outputs = np.array(given_inputs, dtype = np.float64)

        # Feed Forward for each Level
        for level in network.__levels :
            outputs = Level.feed_forward(
                outputs,
                level
            )

        return ControlOutput(*outputs.flat[:4].tolist())

class Level :
    def __init__(self, input_count: int, output_count: int, is_hidden_layer: bool = True) -> None :
        # Set empty vectors and matrix
        self.__inputs = np.empty((input_count, 1), np.float64)
        self.__outputs = np.empty((output_count, 1), np.float64)
        self.__biases = np.empty((output_count, 1), np.float64)
        self.__weights = np.empty((output_count, input_count), np.float64)

        self.__is_hidden_layer = is_hidden_layer

        self.__randomize(self)

    @property
    def inputs (self) -> list[float] :
        return self.__inputs.flat[:].tolist()

    @property
    def outputs (self) -> list[float] :
        return self.__outputs.flat[:].tolist()

    @property
    def biases (self) -> list[float] :
        return self.__biases.flat[:].tolist()

    @property
    def weights (self) -> list[list[float]] :
        return self.__weights.tolist()

    @property
    def is_hidden_layer (self) :
        return self.__is_hidden_layer

    @staticmethod
    def __randomize (level: 'Level') :
        low, high = -1, 1

        # Randomize Weights Matrix
        np.put(
            level.__weights,
            range(level.__weights.size),
            np.random.random(level.__weights.shape) * (high - low) + low,
            mode = 'clip'
        )
        # Randomize Biases Vector
        np.put(
            level.__biases,
            range(level.__biases.size),
            np.random.random(level.__biases.shape) * (high - low) + low,
            mode = 'clip'
        )

    @staticmethod
    def feed_forward (given_inputs: list[float] | npt.NDArray[np.float64], level: 'Level') :
        # Put given inputs to inputs vector
        np.put(
            level.__inputs,
            range(level.__inputs.size),
            given_inputs,
            mode = 'clip'
        )

        # Calculate: W . x
        weight_dot_input = np.empty((level.__outputs.size, 1), np.float64)
        level.__weights.dot(level.__inputs, out = weight_dot_input)

        # Calculate: W.x + b
        np.add(weight_dot_input, level.__biases, out = level.__outputs)

        # Sigmoid Neuron Output
        level.__outputs = sigmoid(level.__outputs)

        if not level.__is_hidden_layer :
            # Activation Function Output
            level.__outputs = (level.__outputs >= 0.5).astype(np.float64)

        return level.__outputs