import dearpygui.dearpygui as dpg

# Placeholder data
xVal = [i for i in range(10)]
yVal = [i*i for i in range(10)]
data = [[150, True], [280, True], [470, True], [600, False], [700, False]]

dpg.create_context()

def find_circle(px: int):
    for i in range(len(data)):
        if abs(data[i][0] - px) < 10:
            return i

    return -1

def mouse_down():
    dpg.set_value("is_mouse_down", True)
    current_circle = dpg.get_value("current_circle")
    if current_circle == -1:
        px, py = dpg.get_mouse_pos(local=False)
        if py > 480 and py < 520:
            index = find_circle(px)
            if index != -1:
                dpg.set_value("current_circle", index)

def mouse_release():
    dpg.set_value("is_mouse_down", False)
    dpg.set_value("current_circle", -1)


def move_circle():
    px, py = dpg.get_mouse_pos(local=False)
    current_circle = dpg.get_value("current_circle")
    if current_circle != -1:
        indexStr = str(current_circle)
        dpg.configure_item(f"circle_{indexStr}", center=[px, 500])
        data[current_circle][0] = px

with dpg.value_registry():
    dpg.add_bool_value(default_value=False, tag="is_mouse_down")
    dpg.add_int_value(default_value=-1, tag="current_circle")

with dpg.handler_registry():
    dpg.add_mouse_move_handler(callback=move_circle)
    dpg.add_mouse_down_handler(callback=mouse_down)
    dpg.add_mouse_release_handler(callback=mouse_release)

with dpg.window(tag="Primary Window",width=800, height=600):
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


    # Custom axis. All elements will be dragable etc.
    # It should be relativley trivial to implement.
    dpg.draw_line([50, 500], [750, 500], color=[200, 200, 200], thickness=2)

    dpg.draw_line([400, 490], [400, 510], color=[230, 230, 230], thickness=4) # Threshold

    for index in range(len(data)):
        indexStr = str(index)
        if data[index][1] == True:
            dpg.draw_circle([data[index][0], 500], radius=10, color=(0, 255, 0), fill=[0, 255, 0], tag=f"circle_{indexStr}")
        else:
            dpg.draw_circle([data[index][0], 500], radius=10, color=(255, 0, 0), fill=[255, 0, 0], tag=f"circle_{indexStr}")

    dpg.add_text("F measure etc...", indent=1, pos=[50, 600])

dpg.create_viewport(title='Custom Title', width=800, height=600, resizable=False)
dpg.setup_dearpygui()

# dpg.show_style_editor()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)

dpg.start_dearpygui()
dpg.destroy_context()