import plotly.graph_objects as graph_obj


class Plot:
    pass


class PlotCurve(Plot):
    pass


class ConfussionMatrix(Plot):
    pass


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
