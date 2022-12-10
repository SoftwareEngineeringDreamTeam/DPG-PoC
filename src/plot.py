# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=unused-import
# pylint: disable=import-error
# pylint: disable=W
import numpy as np
import plotly.graph_objects as graph_obj

from src.__init__ import dpg


class Plot:
    pass


class PlotCurve(Plot):
    def __init__(self, roc={"fpr": np.array([]),
                            "tpr": np.array([])}):
        self.roc = roc
        self.prev_roc = self.roc

    def draw(self):
        with dpg.plot(width=400):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="FP Rate")
            dpg.set_axis_limits(dpg.last_item(), -0.1, 1.1)
            dpg.add_plot_axis(dpg.mvYAxis, label="TP Rate", tag="y_axis")
            dpg.set_axis_limits(dpg.last_item(), -0.1, 1.1)
            dpg.add_line_series(self.prev_roc["fpr"],
                                self.prev_roc["tpr"],
                                label="Previous ROC curve",
                                parent='y_axis',
                                tag="prev_roc_tag")
            dpg.add_line_series(self.roc["fpr"],
                                self.roc["tpr"],
                                label="ROC Curve",
                                parent='y_axis',
                                tag="roc_tag")

    def update(self, roc):
        self.prev_roc = self.roc
        self.roc = roc
        dpg.set_value('roc_tag', [self.roc["fpr"],
                                  self.roc["tpr"]])
        dpg.set_value('prev_roc_tag', [self.prev_roc["fpr"],
                                       self.prev_roc["tpr"]])

    def save_to_png(self):
        fig = graph_obj.Figure()
        fig.add_trace(graph_obj.Scatter(x=self.prev_roc["fpr"],
                      y=self.prev_roc["tpr"],
                      name="Previous ROC Curve",
                      mode='lines'))
        fig.add_trace(graph_obj.Scatter(x=self.roc["fpr"],
                      y=self.roc["tpr"],
                      name="ROC Curve",
                      mode='lines'))
        fig.update_layout(title_text='ROC curve')
        fig.update_xaxes(title_text='FP Rate', range=[-0.01, 1.01])
        fig.update_yaxes(title_text='TP Rate', range=[-0.01, 1.01])
        fig.write_image("ROC_curve.png")


class PlotMatrix(Plot):
    def __init__(self, matrix=np.zeros((2, 2), dtype=int)):
        true_pos = Value("", matrix[0, 0])
        true_neg = Value("", matrix[1, 1])
        false_pos = Value("", matrix[0, 1])
        false_neg = Value("", matrix[1, 0])
        self.vals = [[true_pos, false_pos], [false_neg, true_neg]]

    def draw(self):
        labels = ["Predicted positive", "Predicted negative"]
        with dpg.table(header_row=True, resizable=True,
                       policy=dpg.mvTable_SizingStretchProp,
                       borders_outerH=True, borders_innerV=True,
                       borders_innerH=True, borders_outerV=True):
            dpg.add_table_column(label="")
            dpg.add_table_column(label="Real Positive")
            dpg.add_table_column(label="Real Negative")
            for i in range(0, 2):
                with dpg.table_row():
                    for j in range(0, 3):
                        if j == 0:
                            dpg.add_text(labels[i])
                        else:
                            self.vals[i][j-1].draw()

    def update(self, matrix):
        for i in range(0, 2):
            for j in range(0, 2):
                self.vals[i][j].set_value(matrix[i, j])
                self.vals[i][j].update()


class Value:
    color = [255, 255, 255]
    ui_elem = None

    def __init__(self, name: str, initial_value=0):
        self.name = name
        self.value = initial_value
        self.prev_value = self.value

    def draw(self):
        with dpg.group(horizontal=True):
            if self.name != "":
                dpg.add_text(self.name + ":")
            self.ui_elem = dpg.add_text(self.value, color=self.color)
            dpg.add_spacer(width=10)

    def set_value(self, value):
        self.prev_value = self.value
        self.value = value
        if self.prev_value != self.value:
            self.set_color([255, 0, 0])

        else:
            self.set_color([255, 255, 255])

    def get_value(self):
        return self.value

    def set_color(self, color: list):
        self.color = color

    def update(self):
        if not self.ui_elem:
            return  # should raise exception?

        dpg.configure_item(self.ui_elem, default_value=self.value,
                           color=self.color)
