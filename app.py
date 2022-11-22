import dearpygui.dearpygui as dpg

from data import Data

# Placeholder data for plots
xVal = [i for i in range(10)]
yVal = [i*i for i in range(10)]
data = [[150, True], [280, True], [470, True], [600, False], [750, False]]

# Draggable point variables
point = None
pointPos = [50, 500]

dpg.create_context()

with dpg.window(tag="Primary Window"):
    dpg.add_file_dialog(directory_selector=True, show=False, tag="file_dialog_id")
    dpg.add_button(label="Select File", callback=lambda: dpg.show_item("file_dialog_id"), height=50, width=200)

    dpg.add_spacer(height=20)
    
    with dpg.group(horizontal=True):
        with dpg.plot(width = 400):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="x")
            dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")
            dpg.add_line_series(xVal, yVal, label='Data', parent='y_axis')

        with dpg.plot(width = 400):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="x")
            dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis2")
            dpg.add_line_series(xVal, yVal, label='Data2', parent='y_axis2')

    # Custom 1D graph
    dpg.draw_line([50, 500], [800, 500], color=[200, 200, 200], thickness=2)

    dpg.draw_line([400, 490], [400, 510], color=[230, 230, 230], thickness=4) # Threshold

    for point in data:
        if point[1] == True:
            dpg.draw_circle([point[0], 500], radius=10, color=(0, 255, 0), fill=[0, 255, 0])
        else:
            dpg.draw_circle([point[0], 500], radius=10, color=(255, 0, 0), fill=[255, 0, 0])

    dpg.add_text("F measure etc...", indent=1, pos=[50, 600])

    # Draggable point for testing
    point = dpg.draw_circle(pointPos, radius=10, color=(0, 0, 255), fill=[0, 0, 255])

dpg.create_viewport(title='Classification Metrics Demonstrator', width=850, resizable=False)
dpg.setup_dearpygui()

# dpg.show_style_editor()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)

while dpg.is_dearpygui_running():
    if dpg.is_mouse_button_down(0) and abs(dpg.get_mouse_pos()[0] - pointPos[0]) < 50 and abs(dpg.get_mouse_pos()[1] - pointPos[1]) < 50:
        pointPos[0] = dpg.get_mouse_pos()[0]
        dpg.configure_item(item = point, center=pointPos)

    dpg.render_dearpygui_frame()

# dpg.start_dearpygui() # No need to call when using a render loop
dpg.destroy_context()