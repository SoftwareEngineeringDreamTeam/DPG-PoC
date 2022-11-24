from math import sin

from __init__ import dpg
from data import Data
from axis import Threshold
from utils import generate_example_points


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


class PlotData:
    def __init__(self, x_values: list or tuple, y_values: list or tuple):
        self.x_axis = x_values
        self.y_axis = y_values


if __name__ == "__main__":
    app = App()
    app.run()
