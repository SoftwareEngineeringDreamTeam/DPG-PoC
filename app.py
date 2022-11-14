import dearpygui.dearpygui as dpg
from math import sin, sqrt
from random import randint, choices


class Dragable:
    @staticmethod
    def is_dragable():
        return True


class Point(Dragable):
    y_pos = 500
    radius = 10
    _green = (0, 255, 0)
    _red = (255, 0, 0)

    def __init__(self, pos, val):
        self.x_pos = pos
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


class Threshold(Dragable):
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


def circle_distance(a, b):
    return sqrt((a)**2 + (b)**2)


def bounds_check(point, max_distance=20):
    dist = circle_distance(
        (dpg.get_mouse_pos()[0] - point.x_pos),
        (dpg.get_mouse_pos()[1] - point.y_pos)
    )
    if dist < max_distance:
        return True

    return False


dpg.create_context()
plot_data = PlotData(
    [i/10 for i in range(0, 100, 1)],
    [i*sin(i)/10 for i in range(0, 100, 1)]
)
axis_data = {
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
        with dpg.plot(width=400):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="x")
            dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")
            dpg.add_line_series(
                plot_data.x_axis,
                plot_data.y_axis,
                label='Data',
                parent='y_axis'
            )

        with dpg.plot(width=400):
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

    # Custom axis. All elements will be dragable etc.
    # It should be relativley trivial to implement.
    dpg.draw_line([50, 500], [750, 500], color=[200, 200, 200], thickness=2)

    # Threshold
    axis_data["threshold"].draw()

    # Drawing points
    for point in axis_data["points"]:
        point.draw()

    dpg.add_text("F measure etc...", indent=1, pos=[50, 600])

dpg.create_viewport(
    title='Classification Metrics Demonstrator',
    width=850,
    resizable=False
)
dpg.setup_dearpygui()

# dpg.show_style_editor()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)

holding = False
while dpg.is_dearpygui_running():
    if dpg.is_mouse_button_down(0):
        for point in axis_data["points"]:
            if bounds_check(point) and not holding:
                holding = point
                point.x_pos = dpg.get_mouse_pos()[0]
                dpg.configure_item(
                    item=point.point,
                    center=(point.x_pos - point.radius, point.y_pos)
                )
            elif holding == point:
                point.x_pos = dpg.get_mouse_pos()[0]
                dpg.configure_item(
                    item=point.point,
                    center=(point.x_pos - point.radius, point.y_pos)
                )
    else:
        holding = False
    dpg.render_dearpygui_frame()

dpg.destroy_context()
