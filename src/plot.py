import plotly.graph_objects as graph_obj

from __init__ import dpg


class Plot:
    pass


class PlotCurve(Plot):
    def plot(self, x, y):
        with dpg.plot(width=400):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="FP Rate")
            dpg.add_plot_axis(dpg.mvYAxis, label="TP Rate", tag="y_axis")
            dpg.add_line_series(x, y,
                                label='ROC Curve',
                                parent='y_axis')

    def save_to_png(self, sender, app_data, user_data):
        x, y = user_data
        fig = graph_obj.Figure()
        fig.add_trace(graph_obj.Scatter(x=x,
                      y=y,
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
