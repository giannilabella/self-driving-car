import tkinter as tk

from utils import lerp, get_hex_color
from network import NeuralNetwork, Level

class Visualizer :
    # Drawn Items Lists
    __drawn_items = []

    @classmethod
    def draw_network (cls, canvas: tk.Canvas, network: NeuralNetwork) :
        margin = 75
        left = margin
        top = margin

        width = canvas.winfo_width() - 2 * margin
        height = canvas.winfo_height() - 2 * margin

        level_height = height / len(network.levels)

        # Erase Previously Drawn Items
        for item in cls.__drawn_items :
            canvas.delete(item)
        cls.__drawn_items = []

        # Draw levels
        for index, level in enumerate(network.levels[::-1]) :
            level_top = lerp(
                top, top + height - level_height,
                index / (len(network.levels) - 1)
                if len(network.levels) != 1 else 0.5
            )

            cls.draw_level(
                canvas, level,
                left, level_top, width, level_height,
                ['↑', '←', '→', '↓'] if not level.is_hidden_layer else None
            )

    @classmethod
    def draw_level (cls, canvas: tk.Canvas, level: Level, left: float, top: float, width: float, height: float, labels: list[str] | None = None) :
        right = left + width
        bottom = top + height

        # Drawing parameters
        node_radius = 25
        node_margin = 5
        bias_width = 3

        # Draw Level Weights (Edges)
        for row_index, row in enumerate(level.weights) :
            for column_index, weight in enumerate(row) :
                cls.__drawn_items.append(
                    canvas.create_line(
                        # Input Node
                        cls.__get_node_x(row, column_index, left, right), bottom,
                        # Output Node
                        cls.__get_node_x(level.weights, row_index, left, right), top,
                        fill = get_hex_color(weight), width = 3, dash = (255,),
                ))

        # Draw Level Inputs (Nodes)
        for index, input in enumerate(level.inputs) :
            x = cls.__get_node_x(level.inputs, index, left, right)

            cls.__drawn_items.extend([
                # Margin around Input Node
                canvas.create_oval(
                    x - (node_radius + node_margin), bottom - (node_radius + node_margin),
                    x + (node_radius + node_margin), bottom + (node_radius + node_margin),
                    fill = 'black'
                ),
                # Input Node
                canvas.create_oval(
                    x - node_radius, bottom - node_radius,
                    x + node_radius, bottom + node_radius,
                    fill = get_hex_color(input)
                )
            ])

        # Draw Level Biases (Nodes Outline)
        for index, bias in enumerate(level.biases) :
            x = cls.__get_node_x(level.biases, index, left, right)

            cls.__drawn_items.extend([
                # Margin around Biases
                canvas.create_oval(
                    x - (node_radius + node_margin), top - (node_radius + node_margin),
                    x + (node_radius + node_margin), top + (node_radius + node_margin),
                    fill = 'black'
                ),
                # Bias: Dashed outline around Output Node
                canvas.create_oval(
                    x - node_radius + bias_width / 2, top - node_radius + bias_width / 2,
                    x + node_radius - bias_width / 2, top + node_radius - bias_width / 2,
                    outline = get_hex_color(bias), dash = (255,), width = bias_width
                )
            ])

        # Draw Level Outputs (Nodes)
        for index, output in enumerate(level.outputs) :
            x = cls.__get_node_x(level.outputs, index, left, right)

            cls.__drawn_items.extend([
                # Output Node
                canvas.create_oval(
                    x - node_radius + 2 * bias_width, top - node_radius + 2 * bias_width,
                    x + node_radius - 2 * bias_width, top + node_radius - 2 * bias_width,
                    fill = get_hex_color(output)
                ),
                canvas.create_text(
                    x + 2.5, top + node_radius * 0.04 + 1,
                    text = labels[index], font = ('Fira Code', int(node_radius * 1.2), 'bold'),
                    fill = 'black'
                ) if labels is not None else None,
                canvas.create_text(
                    x, top + node_radius * 0.04,
                    text = labels[index], font = ('Fira Code', int(node_radius * 1.2), 'bold'),
                    fill = get_hex_color(- output / output) if output != 0 else 'white'
                ) if labels is not None else None
            ])

    @staticmethod
    def __get_node_x (nodes: list, index: int, left: float, right: float) :
        return lerp(
            left, right,
            index / (len(nodes) - 1)
            if len(nodes) != 1
            else 0.5
        )

