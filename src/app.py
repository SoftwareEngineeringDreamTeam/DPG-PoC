# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=unused-import
# pylint: disable=import-error
# pylint: disable=W

from src.__init__ import dpg
from src.axis import Axis
from src.data import Data
from src.plot import PlotCurve, PlotMatrix, Value


class App:
    def __init__(self):
        self.metrics_panel = MetricsPanel()
        self.matrix = PlotMatrix()
        self.curve = PlotCurve()
        self.data = Data(self.metrics_panel, self.matrix, self.curve)
        self.axis = Axis(self.data)
        self._prepare_gui()

    def _load_file(self, sender, app_data):
        old_points = self.data.load_points(app_data['file_path_name'])
        self.axis.override_points(old_points)

    def _save_file(self, sender, app_data):
        self.data.save(app_data['file_path_name'])

    def _add_new_point(self, x_pos, value, popup):
        self.data.add_point(x_pos, value)
        self.axis.render_new_point()
        dpg.delete_item(popup)

    def _show_add_point_popup(self, sender, app_data):
        with dpg.window(
                modal=True,
                pos=dpg.get_item_pos(sender),
                no_move=True,
                on_close=lambda: dpg.delete_item(popup)
                ) as popup:
            dpg.add_input_float(
                tag="new_point_x_pos",
                min_value=50,
                max_value=800,
                step=1,
                default_value=0
            )
            dpg.add_checkbox(
                tag="new_point_value",
                label="Class",
                default_value=False,
            )
            dpg.add_spacer(height=10)
            dpg.add_button(
                label="Add",
                width=150,
                callback=lambda sender, app_data, user_data: self._add_new_point(
                    x_pos=dpg.get_value("new_point_x_pos"),
                    value=dpg.get_value("new_point_value"),
                    popup=popup
                )
            )

    def _prepare_gui(self):
        dpg.create_context()

        with dpg.window(tag="Primary Window"):
            with dpg.file_dialog(
                directory_selector=False,
                show=False,
                callback=self._load_file,
                width=600,
                height=400,
                tag="file_loader_id"
            ):
                dpg.add_file_extension(".csv", color=(255, 255, 0, 255))

            with dpg.file_dialog(
                directory_selector=False,
                show=False,
                callback=self._save_file,
                default_filename='res',
                width=600,
                height=400,
                tag="file_saver_id"
            ):
                dpg.add_file_extension(".csv", color=(255, 255, 0, 255))

            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Select file",
                    callback=lambda: dpg.show_item("file_loader_id"),
                    height=50,
                    width=200
                )

                dpg.add_button(
                    label="Save to file",
                    callback=lambda: dpg.show_item("file_saver_id"),
                    height=50,
                    width=200
                )

            dpg.add_button(
                label="Generate random points",
                pos=[640, 10],
                callback=lambda: self.axis.generate_random_points(),
                height=50,
                width=200
            )

            dpg.add_spacer(height=20)

            with dpg.group(horizontal=True):
                self.curve.draw()
                self.matrix.draw()

            dpg.add_button(label="Download the ROC curve",
                           tag="btn_roc",
                           height=50, width=200,)
            dpg.set_item_callback("btn_roc", self.curve.save_to_png)

            self.axis.setup_axis()

            dpg.add_spacer(height=150)

            self.metrics_panel.draw()

            dpg.add_button(
                label="Invert all",
                pos=[670, 530],
                callback=lambda: self.axis.invert_all_points(),
                height=30,
                width=100
            )

            dpg.add_button(
                label="+",
                pos=[780, 530],
                callback=self._show_add_point_popup,
                height=30,
                width=30
            )

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
            "precision": Value("Precision"),
            "balanced_acc": Value("Balanced Accuracy"),
            "mcc": Value("Matthew's correlation coefficient")
        }

    def draw(self):
        with dpg.group(horizontal=True,pos=(0, 600)):
            dpg.add_spacer(width=75)
            with dpg.group():
                self.metrics["f1_score"].draw()
                self.metrics["auc"].draw()
                self.metrics["recall"].draw()
                self.metrics["precision"].draw()

            with dpg.group(pos=[400, 600]):
                self.metrics["accuracy"].draw()
                self.metrics["specificity"].draw()
                self.metrics["balanced_acc"].draw()
                self.metrics["mcc"].draw()

    def update(self, vals):
        for i, value in enumerate(self.metrics.values()):
            score = vals[i]
            if score != "NaN":
                score = round(score, 3)
            value.set_value(score)
            value.update()

    def update_live(self, vals):
        for i, value in enumerate(self.metrics.values()):
            score = vals[i]
            if score != "NaN":
                score = round(score, 3)
            value.set_value_live(score)
            value.update()
