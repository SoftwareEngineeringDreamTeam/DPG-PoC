import dearpygui.dearpygui as dpg


class Dragable:
    @staticmethod
    def is_dragable():
        return True

class Point(Dragable):
    def __init__(self, pos, val):
        self.position = pos
        self.value = val

    def draw_red_point(self):
        pass

    def draw_green_point(self):
        pass

class Threshold(Dragable):
    y_pos = 500
    half_length = 10
    thickness = 4
    color = [230, 230, 230]
    def __init__(self, x_pos):
        self.x_pos = x_pos

    def draw(self):
        # dpg.draw_line([400, 490], [400, 510], color=[230, 230, 230], thickness=4) # Threshold
        dpg.draw_line(
            [self.x_pos, self.y_pos-self.half_length],
            [self.x_pos, self.y_pos+self.half_length],
            color=self.color,
            thickness = self.thickness
        )

class PlotData:
    def __init__(self, x_values, y_values):
        self.x_axis = x_values
        self.y_axis = y_values




plot_data = PlotData(
    [i for i in range(10)],
    [i*i for i in range(10)]
)
data = {
    "points": [[150, True], [280, True], [470, True], [600, False], [750, False]],
    "treshold": {}}

point = None
pointPos = [50, 500]
points = [Point(pointPos, True)]

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
            dpg.add_line_series(plot_data.x_axis, plot_data.y_axis, label='Data', parent='y_axis')

        with dpg.plot(width = 400):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="x")
            dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis2")
            dpg.add_line_series(plot_data.x_axis, plot_data.y_axis, label='Data2', parent='y_axis2')

    # Custom 1D graph
    dpg.draw_arrow([50, 500], [800, 500], color=[200, 200, 200], thickness=2)

    data["treshold"].draw() # Threshold

    for point in data:
        if point[1] == True:
            dpg.draw_circle(
                [point[0], 500],
                radius=10,
                color=(0, 255, 0),
                fill=[0, 255, 0]
            )
        else:
            dpg.draw_circle(
                [point[0], 500],
                radius=10,
                color=(255, 0, 0),
                fill=[255, 0, 0]
            )

    dpg.add_text("F measure etc...", indent=1, pos=[50, 600])

    # Draggable point for testing
    point = dpg.draw_circle(pointPos, radius=10, color=(0, 0, 255), fill=[0, 0, 255])

dpg.create_viewport(title='Classification Metrics Demonstrator', width=850, resizable=False)
dpg.setup_dearpygui()

# dpg.show_style_editor()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)

while dpg.is_dearpygui_running():
    if dpg.is_mouse_button_down(0) and abs(dpg.get_mouse_pos()[0] - pointPos[0]) < 50 and abs(dpg.get_mouse_pos()[1] - pointPos[1]) < 50:
        pointPos[0] = dpg.get_mouse_pos()[0]
        dpg.configure_item(item=point, center=pointPos)

    dpg.render_dearpygui_frame()

# dpg.start_dearpygui() # No need to call when using a render loop
dpg.destroy_context()