import plotly.graph_objects as graph_obj

from __init__ import dpg


class Data:
    def __init__(self):
        self.save_file = "res.csv"

    def update(self):
        pass

    def _update_f1_score(self):
        pass

    def _update_accuracy_score(self):
        pass

    def _update_recall_score(self):
        pass

    def _update_roc_curve(self):
        pass

    def _update_auc_curve(self):
        pass

    def _update_mmc_score(self):
        pass

    def _update_matrix(self):
        pass

    def save(self):
        pass


class Plot:
    def plot(self, x, y):
        pass


class ConfusionMatrix(Plot):
    def plot(self, confusion_matrix):
        pass


class Curve(Plot):
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
