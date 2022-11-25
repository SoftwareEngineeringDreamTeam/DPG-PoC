from math import sin

import plotly.graph_objects as graph_obj

from __init__ import dpg
from axis import Threshold
from data import Data
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

            with dpg.group(horizontal=True):
                dpg.add_button(label="Download the AUC curve",
                               tag="btn_auc",
                               height=50, width=200,)
                dpg.set_item_callback("btn_auc", plot_data.save_to_png)
                dpg.set_item_user_data("btn_auc", "AUC_curve.png")
                dpg.add_spacer(width=193)

                dpg.add_button(label="Download the ROC curve",
                               tag="btn_roc",
                               height=50, width=200,)
                dpg.set_item_callback("btn_roc", plot_data.save_to_png)
                dpg.set_item_user_data("btn_roc", "ROC_curve.png")

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

    def save_to_png(self, sender, app_data, user_data):
        fig = graph_obj.Figure()
        if user_data == "ROC_curve.png":
            fig.add_trace(graph_obj.Scatter(x=self.x_axis,
                          y=self.y_axis,
                          mode='lines'))
            fig.update_layout(title_text='ROC curve')
            fig.update_xaxes(title_text='x')
            fig.update_yaxes(title_text='y')
        else:
            fig.add_trace(graph_obj.Scatter(x=self.x_axis,
                          y=self.y_axis,
                          mode='lines'))
            fig.update_layout(title_text='AUC curve')
            fig.update_xaxes(title_text='x')
            fig.update_yaxes(title_text='y')
        fig.write_image(user_data)


if __name__ == "__main__":
    app = App()
    app.run()
