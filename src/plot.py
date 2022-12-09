# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=unused-import
# pylint: disable=import-error
# pylint: disable=W

import plotly.graph_objects as graph_obj

from src.__init__ import dpg


class Plot:
    pass


class PlotCurve(Plot):
    def plot(self, x_val, y_val):
        with dpg.plot(width=400):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="FP Rate")
            dpg.add_plot_axis(dpg.mvYAxis, label="TP Rate", tag="y_axis")
            dpg.add_line_series(x_val, y_val,
                                label='ROC Curve',
                                parent='y_axis')

    def save_to_png(self, sender, app_data, user_data):
        x_val, y_val = user_data
        fig = graph_obj.Figure()
        fig.add_trace(graph_obj.Scatter(x=x_val,
                      y=y_val,
                      mode='lines'))
        fig.update_layout(title_text='ROC curve')
        fig.update_xaxes(title_text='FP Rate')
        fig.update_yaxes(title_text='TP Rate')
        fig.write_image("ROC_curve.png")


class PlotMatrix(Plot):
    def plot(self, confusion_matrix):
        labels = ["Predicted positive", "Predicted negative"]
        with dpg.table(header_row=True, resizable=True,
                       policy=dpg.mvTable_SizingStretchProp,
                       borders_outerH=True, borders_innerV=True,
                       borders_innerH=True, borders_outerV=True):
            dpg.add_table_column(label="")
            dpg.add_table_column(label="Real Positive")
            dpg.add_table_column(label="Real Negative")

            # once it reaches the end of the columns
            for i in range(0, 2):
                with dpg.table_row():
                    for j in range(0, 3):
                        if j == 0:
                            dpg.add_text(labels[i])
                        else:
                            dpg.add_text(confusion_matrix[i, j-1])


class PlotData:
    def __init__(self, x_values: list or tuple, y_values: list or tuple):
        self.x_axis = x_values
        self.y_axis = y_values


class Value:
    color = [255, 255, 255]

    def __init__(self, name: str, initial_value = 0):
        self.name = name
        self.value = initial_value

    def draw(self):
        with dpg.group(horizontal=True):
            dpg.add_text(self.name + ":")
            self.ui_elem = dpg.add_text(self.value, color = self.color)
            dpg.add_spacer(width=10)

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_color(self, color: list):
        self.color = color

    def update(self):
        if not self.ui_elem:
            return  # should raise exception?

        dpg.configure_item(self.ui_elem, default_value=self.value, color=self.color)