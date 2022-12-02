# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=unused-import
# pylint: disable=import-error

from math import sqrt

from __init__ import dpg
from utils import generate_example_points


class Axis:
    thickness=None

    def __init__(self, data_ref):
        self.data_ref = data_ref
        self.data = {
            "points": generate_example_points((150, 750), Point),
            "threshold": 400
        }

    def setup_axis(self):
        
        # Custom 1D graph
        dpg.draw_arrow(
            [800, 500],
            [50, 500],
            color=[200, 200, 200],
            thickness=2
        )

        # Threshold
        Threshold(self.data["threshold"]).draw()

        # Drawing points
        for point in self.data["points"]:
            point.draw()

        dpg.add_text("F measure etc...", indent=1, pos=[50, 600])

    def add_point(self):
        pass

    def delete_point(self, point):
        pass

    def draw(self):
        pass

    def check_interaction(self):
        holding = False

        while dpg.is_dearpygui_running():
            if dpg.is_mouse_button_down(0):  # Left button
                for point in self.data["points"]:
                    if point.bounds_check() and not holding:
                        holding = point
                        point.update_dragged_point()
                    elif holding == point:
                        point.update_dragged_point()

            elif dpg.is_mouse_button_down(1):  # Right button
                for point in self.data["points"]:
                    if point.bounds_check():
                        self.__show_popup_for(point)

            else:
                holding = False

            dpg.render_dearpygui_frame()

    def __show_popup_for(self, item):
        with dpg.window(
                modal=True,
                pos=item.get_position(),
                no_move=True,
                on_close=lambda: dpg.delete_item(popup)
            ) as popup:
            if isinstance(item, Point):
                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Delete",
                        user_data=item,
                        callback=lambda sender, app_data, user_data: self.delete_point(user_data)
                    )
                    dpg.add_checkbox(
                        label="Class",
                        default_value=item.get_value(),
                        callback=item.flip_class()
                    )

                dpg.add_input_float(
                    min_value=0,
                    max_value=1
                )

            elif isinstance(item, Threshold):
                dpg.add_input_float(
                    min_value=0,
                    max_value=1
                )


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

    def get_value(self):
        return self.value

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
