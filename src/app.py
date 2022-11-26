from math import sin


from __init__ import dpg
from axis import Axis
from plot import PlotData

class App:
    def __init__(self):
        self.data = None
        self.axis = Axis(self.data)
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

            self.axis.setup_axis()

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
