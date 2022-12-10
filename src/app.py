# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=unused-import
# pylint: disable=import-error
# pylint: disable=W

from math import sin

import numpy as np

from src.data import Data
from src.__init__ import dpg
from src.axis import Axis
from src.plot import PlotCurve, PlotData, PlotMatrix, Value


class App:
    def __init__(self):
        self.data = Data()
        self.axis = Axis(self.data)
        self.curve = PlotCurve()
        self.matrix = PlotMatrix()
        self._prepare_gui()

    def _load_file(self, sender, app_data):
        old_points = self.data.load_points(app_data['file_path_name'])
        self.axis.override_points(old_points)

    def _prepare_gui(self):
        dpg.create_context()
        plot_data = PlotData(
            [i/10 for i in range(0, 100, 1)],
            [i*sin(i)/10 for i in range(0, 100, 1)]
        )

        with dpg.window(tag="Primary Window"):
            with dpg.file_dialog(
                directory_selector=False,
                show=False,
                callback=self._load_file,
                tag="file_dialog_id"
            ):
                dpg.add_file_extension(".csv", color=(255, 255, 0, 255))

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

            dpg.add_spacer(height=150)

            metrics_panel = MetricsPanel()

    def run(self):
        dpg.create_viewport(
            title='Classification Metrics Demonstrator',
            width=850,
            resizable=False
        )
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Primary Window", True)

        # Main render loop
        while dpg.is_dearpygui_running():
            self.axis.check_interaction()
            dpg.render_dearpygui_frame()

        dpg.destroy_context()


class MetricsPanel:
    def __init__(self):
        self.metrics = {
            "f1_score": Value("F1 Score"),
            "auc": Value("AUC"),
            "accuracy": Value("Accuracy"),
            "specificity": Value("Specificity"),
            "recall": Value("Recall"),
            "precision": Value("Precision")
        }
        self.group_split()

    def group_split(self):
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=75)
            with dpg.group():
                self.metrics["f1_score"].draw()
                self.metrics["auc"].draw()

            dpg.add_spacer(width=150)
            with dpg.group():
                self.metrics["accuracy"].draw()
                self.metrics["specificity"].draw()

            dpg.add_spacer(width=150)
            with dpg.group():
                self.metrics["recall"].draw()
                self.metrics["precision"].draw()
