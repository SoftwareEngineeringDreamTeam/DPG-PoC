# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods

from math import sin, sqrt
from random import randint, choices
import dearpygui.dearpygui as dpg

from data import Data

class App:
    def __init__(self):
        self.data = None
        self.axis = None
        self._prepare_gui()

    def _prepare_gui(self):
        dpg.create_context()
        plot_data = PlotData(
            [i/10 for i in range(0, 100, 1)],
            [i*sin(i)/10 for i in range(0, 100, 1)]
        )
        self.data = {
            "points": generate_example_points((150, 750)),
            "threshold": Threshold(400)
        }

        with dpg.window(tag="Primary Window"):
            dpg.add_file_dialog(
                directory_selector=True,
                show=False,
                tag="file_dialog_id"
            )
            dpg.add_button(
                label="Select File",
                callback=lambda: dpg.show_item("file_dialog_id"),
                height=50,
                width=200
            )

            dpg.add_spacer(height=20)

            with dpg.group(horizontal=True):
                with dpg.plot(width = 400):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, label="x")
                    dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")
                    dpg.add_line_series(
                        plot_data.x_axis,
                        plot_data.y_axis,
                        label='Data',
                        parent='y_axis'
                    )

                with dpg.plot(width = 400):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, label="x")
                    dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis2")
                    dpg.add_line_series(
                        plot_data.x_axis,
                        plot_data.y_axis,
                        label='Data2',
                        parent='y_axis2'
                    )

            # Custom 1D graph
            dpg.draw_arrow(
                [800, 500],
                [50, 500],
                color=[200, 200, 200],
                thickness=2
            )

            # Threshold
            self.data["threshold"].draw()

            # Drawing points
            for point in self.data["points"]:
                point.draw()

            dpg.add_text("F measure etc...", indent=1, pos=[50, 600])


    def run(self):
        dpg.create_viewport(title='Classification Metrics Demonstrator', width=850, resizable=False)
        dpg.setup_dearpygui()

        # dpg.show_style_editor()
        dpg.show_viewport()
        dpg.set_primary_window("Primary Window", True)

        holding = False
        while dpg.is_dearpygui_running():
            if dpg.is_mouse_button_down(0):
                for point in self.data["points"]:
                    if point.bounds_check() and not holding:
                        holding = point
                        point.update_dragged_point()
                    elif holding == point:
                        point.update_dragged_point()
            else:
                holding = False
            dpg.render_dearpygui_frame()

    def __del__(self):
        dpg.destroy_context()


class Entity:
    y_pos = 500
    _green = (0, 255, 0)
    _red = (255, 0, 0)
    def __init__(self, x_pos, color, half_length):
        self.x_pos = x_pos
        self.color = color
        self.half_length = half_length

    def set_position(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def get_position(self):
        return self.x_pos, self.y_pos

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def set_half_length(self, half_length):
        self.half_length = half_length

    def get_half_length(self):
        return self.half_length


class Point(Entity):
    radius = 10

    def __init__(self, x_pos, val):
        if val:
            super().__init__(x_pos, self._green, self.radius)
        else:
            super().__init__(x_pos, self._red, self.radius)
        self.value = val
        self.point = None

    def draw(self):
        if self.value:
            self.draw_green_point()
        else:
            self.draw_red_point()

    def draw_red_point(self):
        self.point = dpg.draw_circle(
            (self.x_pos, self.y_pos),
            radius=self.radius,
            color=self._red,
            fill=self._red
        )

    def draw_green_point(self):
        self.point = dpg.draw_circle(
            (self.x_pos, self.y_pos),
            radius=self.radius,
            color=self._green,
            fill=self._green
        )

    def update_dragged_point(self):
        self.x_pos = dpg.get_mouse_pos()[0]
        dpg.configure_item(
            item=self.point,
            center=(self.x_pos - self.radius, self.y_pos)
        )

    def flip_class(self):
        self.value = not self.value

    def _circle_distance(self, a, b):
        return sqrt((a)**2 + (b)**2)

    def bounds_check(self, max_distance=20):
        dist = self._circle_distance(
            (dpg.get_mouse_pos()[0] - self.x_pos - self.radius/2),
            (dpg.get_mouse_pos()[1] - self.y_pos)
        )
        if dist < max_distance:
            return True

        return False


class Threshold:
    y_pos = 500
    half_length = 10
    thickness = 4
    color = [230, 230, 230]

    def __init__(self, x_pos):
        self.x_pos = x_pos

    def draw(self):
        dpg.draw_line(
            [self.x_pos, self.y_pos-self.half_length],
            [self.x_pos, self.y_pos+self.half_length],
            color=self.color,
            thickness=self.thickness
        )


class PlotData:
    def __init__(self, x_values, y_values):
        self.x_axis = x_values
        self.y_axis = y_values


def generate_example_points(
        x_range: tuple,
        nr_of_points: int = 10,
        true_or_false_prc: float = 0.5
        ):
    return [
        Point(
            randint(*x_range),
            choices(
                [False, True],
                [1-true_or_false_prc, true_or_false_prc]
            )[0]
        ) for i in range(nr_of_points)
    ]



if __name__ == "__main__":
    app = App()
    app.run()
