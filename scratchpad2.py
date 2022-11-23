import dearpygui.dearpygui as dpg
import json

# set cwd to this file's directory
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


dpg.create_context()
dpg.create_viewport(title='ScratchPad',width=820, height=520,x_pos=-600,y_pos=100)
dpg.setup_dearpygui()

with dpg.font_registry():
    with dpg.font("C:/Windows/Fonts/msyh.ttc", 24, tag="custom font"):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
    dpg.bind_font(dpg.last_container())

with open('format_string.json', 'r') as f:
    format_string_list=json.load(f)


with dpg.theme() as global_theme:

    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 140, 23), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

    with dpg.theme_component(dpg.mvInputInt):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (140, 255, 23), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

dpg.bind_theme(global_theme)

def save_to_format_string_list(sender,data):
    data=dpg.get_value('format_string')
    if not data:
        return

    print(data)
    global format_string_list
    data = data.split(',')
    format_string_list[data[0]] = data[1]
    # set combo value to this item
    # print(format_string_list)
    with open('format_string_list.json','w') as f:
        json.dump(format_string_list,f)

    dpg.configure_item('format_combo',items= list(format_string_list.keys()))
    dpg.set_value('format_combo', data[0])

def fn(x):
    x=eval(x)
    fmt_string=dpg.get_value('format_combo')
    # print(fmt_string)
    fmt_string=format_string_list[fmt_string]
    return fmt_string.format(x=x)

def calculate(sender,data):
    print(data)
    data=dpg.get_value(sender)
    rs=data.split('\n')
    rs=[fn(x) for x in rs if x]
    dpg.set_value('output', '\n'.join(rs))

def reset_result(sender,data):
    dpg.set_value('format_string',f'{dpg.get_value("format_combo")},{format_string_list[dpg.get_value("format_combo")]}')
    calculate('input',dpg.get_value('input'))

with dpg.window(no_title_bar=True, width=800, height=500):
         # add format string input_text for out put
    with dpg.group(horizontal=True):
        fmt_input=dpg.add_input_text(tag='format_string') 
        dpg.add_button(label="Save format string", callback=save_to_format_string_list)

    # add dropdown for saved format string
    dpg.add_combo(label="result format",tag='format_combo',callback=reset_result, items=list(format_string_list.keys()),default_value=list(format_string_list.keys())[0])

    with dpg.group(horizontal=True):


        dpg.add_input_text( multiline=True,callback=calculate, height=400,tag='input')
        dpg.add_input_text(tag='output', multiline=True, readonly=True,height=400)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()