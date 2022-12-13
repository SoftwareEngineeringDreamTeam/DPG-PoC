# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=unused-import
# pylint: disable=import-error
# pylint: disable=W

import copy

from math import sqrt

from src.__init__ import dpg


class Axis:
    thickness = None
    holding = False

    def __init__(self, data_ref):
        self.data_ref = data_ref
        self.choosen_value = True
        self.start = 50
        self.end = 800

    def setup_axis(self):
        self.data_ref.init_axis_data()
        self.draw()

    def generate_random_points(self):
        old_points = copy.deepcopy(self.data_ref.points)
        self.data_ref.generate_random_points(self.start, self.end)
        self.override_points(old_points)
        self.data_ref.update()

    def add_point(self, mouse_x_position):
        self.data_ref.add_point(mouse_x_position, self.choosen_value)

    def update_point(self, point):
        point.update_dragged_point()
        self.data_ref.update_point_moved()

    def render_new_point(self):
        self.data_ref.points[-1].draw()

    def delete_point(self, point, popup):
        dpg.delete_item(popup)
        point.delete()
        self.data_ref.delete_point(point)

    def invert_all_points(self):
        for point in self.data_ref.points:
            point.flip_class()

        self.data_ref.update()

    def override_points(self, old_points):
        for old_point in old_points:
            old_point.delete()
        for new_point in self.data_ref.points:
            new_point.draw()

    def draw_points(self):
        # Drawing points
        for point in self.data_ref.points:
            point.draw()

    def draw(self):

        # Custom 1D graph
        dpg.draw_arrow(
            [self.end, 500],
            [self.start, 500],
            color=[200, 200, 200],
            thickness=2
        )

        # Threshold
        self.data_ref.threshold.draw()

        self.draw_points()

    def check_axis_limits(self):
        return dpg.get_mouse_pos()[0] >= self.start and dpg.get_mouse_pos()[0] <= self.end

    def check_interaction(self):
        if dpg.is_mouse_button_down(0) and self.check_axis_limits():  # Left button
            threshhold = self.data_ref.threshold
            if threshhold.bounds_check() and not self.holding:
                self.holding = threshhold
                threshhold.update_dragged_threshhold()
                self.data_ref.update()
            elif self.holding == threshhold:
                threshhold.update_dragged_threshhold()
                self.data_ref.update()
            else:
                for point in self.data_ref.points:
                    if point.bounds_check() and not self.holding:
                        self.data_ref.update()
                        self.holding = point
                        self.update_point(point)
                    elif self.holding == point:
                        self.update_point(point)

        elif dpg.is_mouse_button_down(1):  # Right button
            for point in self.data_ref.points:
                if point.bounds_check():
                    self.__show_popup_for(point)

        else:
            self.holding = False

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
                        callback=lambda sender, app_data, user_data: self.delete_point(item, popup)
                    )
                    dpg.add_checkbox(
                        label="Class",
                        default_value=item.get_value(),
                        callback=lambda sender, app_data, user_data: item.flip_class()
                    )

                dpg.add_input_float(
                    min_value=50,
                    max_value=800,
                    step=1,
                    default_value=item.get_position()[0],
                    callback=lambda sender, app_data, user_data:
                        item.update_point_position(app_data)
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
        self.point = dpg.draw_circle(
            (self.x_pos, self.y_pos),
            radius=self.radius,
            color=self.color,
            fill=self.color,
            parent='Primary Window'
            # 'parent could not be deduced' error without it
            # when loading new points
        )

    def update_dragged_point(self):
        self.x_pos = dpg.get_mouse_pos()[0]
        dpg.configure_item(
            item=self.point,
            center=(self.x_pos - self.radius, self.y_pos)
        )

    def update_point_position(self, x_pos):
        self.set_position(x_pos, self.y_pos)
        dpg.configure_item(
            self.point,
            center=(self.x_pos - self.radius, self.y_pos)
        )

    def flip_class(self):
        self.value = not self.value

        if self.value:
            self.color = self._green
        else:
            self.color = self._red

        dpg.configure_item(
            self.point,
            color=self.color,
            fill=self.color
        )

    def get_value(self):
        return self.value

    def _circle_distance(self, point_a, point_b):
        return sqrt((point_a)**2 + (point_b)**2)

    def bounds_check(self, max_distance=20):
        dist = self._circle_distance(
            (dpg.get_mouse_pos()[0] - self.x_pos - self.radius/2),
            (dpg.get_mouse_pos()[1] - self.y_pos)
        )
        if dist < max_distance:
            return True

        return False

    def delete(self):
        dpg.delete_item(self.point)


class Threshold(Entity):

    def __init__(self, x_pos):
        super().__init__(x_pos, (230, 230, 230), 10)
        self.thickness = 6
        self.line = None

    def draw(self):
        self.line = dpg.draw_line(
            p1=[self.x_pos, self.y_pos - self.half_length],
            p2=[self.x_pos, self.y_pos + self.half_length],
            color=self.color,
            thickness=self.thickness
        )

    def bounds_check(self):
        mouse_x = dpg.get_mouse_pos()[0]
        mouse_y = dpg.get_mouse_pos()[1]
        upper_y = self.y_pos + self.half_length
        lower_y = self.y_pos - self.half_length * 2
        upper_x = self.x_pos + self.thickness * 2
        lower_x = self.x_pos - self.thickness * 2
        if lower_y <= mouse_y <= upper_y:
            return lower_x <= mouse_x <= upper_x

        return False

    def update_dragged_threshhold(self):
        self.x_pos = dpg.get_mouse_pos()[0]
        dpg.configure_item(
            item=self.line,
            p1=[self.x_pos - self.thickness * 3 / 2, self.y_pos - self.half_length],
            p2=[self.x_pos - self.thickness * 3 / 2, self.y_pos + self.half_length]
        )
