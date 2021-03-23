from PIL import Image
from config import color_dict
import io

def memory_img_to_io(img, maxsize=(1200, 850)):
    """
    Generate image analysis using PIL
    """
    img.thumbnail(maxsize)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

def file_img_to_io(path, maxsize=(1200, 850)):
    """
    Generate image analysis using PIL
    """
    img = Image.open(path)
    img.thumbnail(maxsize)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

def blank_image():
    img = Image.new('RGB', (1200, 850), (255, 255, 255))
    bio = io.BytesIO()
    img.save(bio, format='PNG')
    return bio.getvalue()

def int_validation(value):
    try:
        int(value)
        return True
    except:
        return False

def create_color_rectangle(color_dict):
    for rgb, name, type in zip(color_dict['rgb'].values(),
                               color_dict['lego_color'].values(),
                               color_dict['type'].values()):
        rect_img = Image.new('RGB', (15, 15), tuple(rgb))
        rect_img.save(f"assets/{type}__{name.replace(' ', '_')}.png")



if __name__ == '__main__':
    create_color_rectangle(color_dict)

# def create_color_rectangle_pil():
#     checkbox_list = []
#     for i, (k, v) in enumerate(colors.items()):
#         col = ImageColor.getrgb(v)
#         rect_img = Image.new('RGB', (5,5), col)
#         checkbox_list += [sg.Checkbox(k, key=f"-C{i}-"),
#                           sg.Image(analysis=memory_img_to_io(rect_img, (5, 5)), key=f"-rect{i}-")]
#
#     return checkbox_list

