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


class ConfussionMatrix(Plot):
    def plot(self, confusion_matrix):
        pass


class PlotData:
    def __init__(self, x_values: list or tuple, y_values: list or tuple):
        self.x_axis = x_values
        self.y_axis = y_values
