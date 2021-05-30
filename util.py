from PIL import Image
import io


def memory_img_to_io(img, maxsize=(1200, 850)):
    """Convert image from memory to bytesIO

    Args:
        img: image in memory
        maxsize: image size for resizing before converting it

    Returns:
        bytes IO file in memory
    """
    img.thumbnail(maxsize)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()


def file_img_to_io(path, maxsize=(1200, 850)):
    """Convert image from disk to bytesIO. First it is read by PIL to memory

    Args:
        path: path of input image
        maxsize: image size for resizing before converting it

    Returns:
        bytes IO file in memory
    """
    img = Image.open(path)
    img.thumbnail(maxsize)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()


def blank_image():
    """ Creating a blank image to the GUI with given size as a BIO file in memory

    Returns:
        The BIO blank file in memory
    """
    img = Image.new('RGB', (1200, 850), (255, 255, 255))
    bio = io.BytesIO()
    img.save(bio, format='PNG')
    del img
    return bio.getvalue()


def int_validation(value):
    """ Checking integer value

    Args:
        value: input value

    Returns:
        True if the input value is int, otherwise False
    """
    try:
        int(value)
        return True
    except:
        return False


def create_color_rectangle(color_dict):
    """ Creating small thumbnail iamges with all the given colors to the GUI.

    Image are saved to the assets folder within the project. It has already been created,
    no need to rerun it.

    Args:
        color_dict: dictionary with colors for which thumbnails are created

    Returns:
        No return value
    """
    for rgb, name, color_type in zip(color_dict['rgb'].values(),
                                     color_dict['lego_color'].values(),
                                     color_dict['type'].values()):
        rect_img = Image.new('RGB', (15, 15), tuple(rgb))
        rect_img.save(f"assets/{type}__{name.replace(' ', '_')}.png")
