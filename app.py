import PySimpleGUI as sg
import os
from main import Legolize
from util import memory_img_to_io, file_img_to_io, int_validation, blank_image
from config import color_dict


sg.change_look_and_feel('LightGrey1')
def text_label(text_var): return sg.Text(text_var + ':', justification='r', size=(25, 1))


# Image part of the layout
image_layout = [
    [sg.Text("Legolized image")],
    [sg.Image(data=blank_image(), key="-image-")],
]

# Setting part of the layout
settings_layout = [
    [sg.Text("Settings")],
    [text_label("Select an image"), sg.Input(key="-filepath-"), sg.FileBrowse(file_types=(("*.png", "*.jpg"),))],
    [text_label("Nr of bricks along the longer side"), sg.Input(32, key="-bricks-")],
    [text_label("Select lego brick type"),
     sg.Radio('Plate', "R1", key="-R1-", default=True), sg.Radio('Round', "R1", key="-R2-"),
     sg.Radio('Tile', "R1", key="-R3-"), sg.Radio('Round tile', "R1", key="-R4-")],
    [text_label("Select base plate color"),
     sg.Radio('Grey', "R2", key="-B1-", default=True), sg.Radio('White', "R2", key="-B2-"),
     sg.Radio('Black', "R2", key="-B3-"), sg.Radio('Green', "R2", key="-B4-")],
    [text_label("Name of the legolized image"), sg.Input(key="-name-")],
    [text_label("Select a folder to save the image"), sg.Input(key="-savepath-"),
     sg.FolderBrowse(), sg.Button("Save image")],
    [text_label(""), sg.Button("Legolize"), sg.Button("Show bricks"), sg.Exit()],
    [sg.Text(key='-status-', justification='r', size=(25, 1))],
]

# Checkbox to select all or none of the color types
color_all_layout = [
    [sg.Checkbox("Solid colors", key="-gCBsolid-", default=True, enable_events=True),
     sg.Checkbox("Transparent colors", key="-gCBtrans-", default=True, enable_events=True),
     sg.Checkbox("Special colors", key="-gCBspec-", default=True, enable_events=True)]
]

# Color layouts
color_layout1 = [
    [sg.Image(data=file_img_to_io(os.path.join('assets', f"{btype}__{color.replace(' ', '_')}.png"), (15, 15))),
     sg.Checkbox(color, key=f"-sCBsolid_{cid}-", default=True)]
    for cid, btype, color in zip(color_dict['lego_color'].keys(),
                                 color_dict['type'].values(),
                                 color_dict['lego_color'].values())
    if btype == "Solid"
]

color_layout2 = [
    [sg.Image(data=file_img_to_io(os.path.join('assets', f"{btype}__{color.replace(' ', '_')}.png"), (15, 15))),
     sg.Checkbox(color, key=f"-sCBtrans_{cid}-", default=True)]
    for cid, btype, color in zip(color_dict['lego_color'].keys(),
                                 color_dict['type'].values(),
                                 color_dict['lego_color'].values())
    if btype == "Transparent"
]

color_layout3 = [
    [sg.Image(data=file_img_to_io(os.path.join('assets', f"Special__{color.replace(' ', '_')}.png"), (15, 15))),
     sg.Checkbox(color, key=f"-sCBspec_{cid}-", default=True)]
    for cid, btype, color in zip(color_dict['lego_color'].keys(),
                                 color_dict['type'].values(),
                                 color_dict['lego_color'].values())
    if btype != "Solid" and btype != "Transparent"
]

# Merging color layouts to a tab group
tab_layout = [
    [sg.TabGroup([[sg.Tab('Solid colors', color_layout1),
                   sg.Tab('Transparent colors', color_layout2),
                   sg.Tab('Special colors', color_layout3)]]
                 )
     ]
]

# Final layout consists of two columns
layout = [
    [
        sg.Column(color_all_layout + tab_layout, key="-COL1-"),
        sg.VSeperator(),
        sg.Column(image_layout + settings_layout, key="-COL2-"),
    ]
]

window = sg.Window("Legolize imgage", layout)

solid, trans, spec = True, True, True

while True:
    event, value = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    # High-level checkbox changes the status of the individual color checkboxes
    elif event == "-gCBsolid-":
        key_solid = [k for k in value.keys() if str(k).startswith('-sCBsolid_')]
        solid = not solid
        for k in key_solid:
            window[k].update(solid)
    elif event == "-gCBtrans-":
        key_strans = [k for k in value.keys() if str(k).startswith('-sCBtrans_')]
        trans = not trans
        for k in key_strans:
            window[k].update(trans)
    elif event == "-gCBspec-":
        key_spec = [k for k in value.keys() if str(k).startswith('-sCBspec_')]
        spec = not spec
        for k in key_spec:
            window[k].update(spec)

    elif event == "Legolize":
        try:
            key_color = [k for k in value.keys() if str(k).startswith('-sCB')]
            color_id = [k.split("_")[1].split('-')[0] for k in key_color if value[k]]
            used_color_list = [rgb for cid, rgb in zip(color_dict['rgb'].keys(), color_dict['rgb'].values())
                               if str(cid) in color_id]
            used_color_dict = {'rgb': used_color_list}

            if int_validation(value["-bricks-"]):
                brick_size = int(value["-bricks-"])
                # Brick type
                if value["-R1-"]:
                    brick_type = "plate"
                elif value["-R2-"]:
                    brick_type = "round"
                elif value["-R3-"]:
                    brick_type = "tile"
                else:
                    brick_type = "round tile"

                # Base plate color
                if value["-B1-"]:
                    # Grey base plate
                    base_plate_color = (150, 150, 150)
                elif value["-B2-"]:
                    # White base plate
                    base_plate_color = (244, 244, 244)
                elif value["-B3-"]:
                    # Black base plate
                    base_plate_color = (27, 42, 52)
                else:
                    # Green base plate
                    base_plate_color = (88, 171, 65)

                if value["-filepath-"] is not None:
                    lg = Legolize(value["-filepath-"], brick_type, brick_size)
                    lg.create_image(used_color_dict, base_plate_color)
                else:
                    sg.popup('Select an image before legolizing!')
            else:
                sg.popup('Number of bricks should be integer, pls change it')
            window["-image-"].update(data=memory_img_to_io(lg.lego_image))
            window['-status-'].update("Legolization has been finished!")
        except Exception as e:
            sg.popup(f"Unexpected error: {e}")
            raise e

    elif event == "Show bricks":
        if lg.brick_nr:
            text = ''
            for k, v in lg.brick_nr.items():
                text += f"Color {k}: {v} piece(s)\n"
            sg.popup_scrolled("Used brick numbers", text)
        else:
            sg.popup("Legolize first!")

    elif event == "Save image":
        filepath = value["-savepath-"]
        filename = value["-name-"] + ".png"
        file = os.path.join(filepath, filename)
        lg.save_image(file)
        window['-status-'].update("Image saved!")

window.close()
