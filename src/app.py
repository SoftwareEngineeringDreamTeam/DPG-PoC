from math import sin
import numpy as np

from __init__ import dpg
from axis import Axis
from plot import PlotData, PlotCurve, PlotMatrix


class App:
    def __init__(self):
        self.data = None
        self.axis = Axis(self.data)
        self.curve = PlotCurve()
        self.matrix = PlotMatrix()
        self._prepare_gui()

    def _prepare_gui(self):
        dpg.create_context()
        plot_data = PlotData(
            [i/10 for i in range(0, 100, 1)],
            [i*sin(i)/10 for i in range(0, 100, 1)]
        )

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
                self.curve.plot(plot_data.x_axis, plot_data.y_axis)
                self.matrix.plot(np.array([[1, 2], [3, 4]]))

            dpg.add_button(label="Download the ROC curve",
                           tag="btn_roc",
                           height=50, width=200,)
            dpg.set_item_callback("btn_roc", self.curve.save_to_png)
            dpg.set_item_user_data("btn_roc",
                                   [plot_data.x_axis, plot_data.y_axis])

            self.axis.setup_axis()
            dpg.add_text("F measure etc...", indent=1, pos=[50, 600])

    def run(self):
        dpg.create_viewport(
            title='Classification Metrics Demonstrator',
            width=850,
            resizable=False
        )
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Primary Window", True)
        self.axis.check_interaction()

    def __del__(self):
        dpg.destroy_context()


if __name__ == "__main__":
    app = App()
    app.run()
