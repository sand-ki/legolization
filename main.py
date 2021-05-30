from PIL import Image
from config import color_dict


class Legolize:
    def __init__(self, path, brick_type, brick_size):
        self.img_path = path
        self.img = Image.open(self.img_path)
        self.brick_type = brick_type
        self.brick_size = brick_size
        self.brick_img = None
        self.lego_image = None
        self.brick_nr = None

    def brick_style(self):
        """ Method for reading the chosen lego image to memory

        Returns:
            No return
        """
        if self.brick_type == "plate":
            self.brick_img = Image.open("assets/lego_plate.png")
        elif self.brick_type == "round":
            self.brick_img = Image.open("assets/lego_stud.png")
        elif self.brick_type == "tile":
            self.brick_img = Image.open("assets/lego_flat_tile.png")
        elif self.brick_type == "round tile":
            self.brick_img = Image.open("assets/lego_stud_flat.png")
        else:
            raise AttributeError("Non-valid brick type. You can choose plate, round, tile or round tile.")

    def brick_sizer(self, img_tranform):
        """ Resizing the image to match the squared lego brick image

        Args:
            img_tranform: input image

        Returns:
            brick_img_s: size of the lego bricks
            brick_nr_w: number of lego bricks width-wise
            brick_nr_h: number of lego bricks height-wise
        """
        img_size = self.img.size
        if img_size[0] >= img_size[1]:
            brick_img_s = int(img_size[0]/img_tranform.size[0])
            brick_nr_w = img_tranform.size[0]
            brick_nr_h = img_tranform.size[1]
        else:
            brick_img_s = int(img_size[1]/img_tranform.size[1])
            brick_nr_w = img_tranform.size[0]
            brick_nr_h = img_tranform.size[1]

        return brick_img_s, brick_nr_w, brick_nr_h

    @staticmethod
    def create_color_palette(color_dictionary):
        """ Create color palette, a list, from the colors selected by the user

        Args:
            color_dictionary: dict with colors selected on the GUI

        Returns:
            color_list: list of colors
            color_nr: number of colors
        """
        color_list = []
        for c in color_dictionary['rgb']:
            color_list.append(c[0])
            color_list.append(c[1])
            color_list.append(c[2])

        color_nr = len(color_dictionary['rgb'])

        return color_list, color_nr

    @staticmethod
    def quantize_color_matching(image, palette, color_nr):
        """ Recoloring image with custom colors using the PIL quantize function

        Args:
            image: thumbnailed input image
            palette: palette with custom colors to be used in the new image
            color_nr: number of colors used

        Returns:
            The recolored image
        """
        pal_img = Image.new("P", (1, 1))
        pal_img.putpalette(palette)

        return image.quantize(palette=pal_img, colors=color_nr).convert("RGB")

    @staticmethod
    def convert_color_matching(image, palette):
        """ Recoloring image with custom colors using the PIL convert function

        Args:
            image: thumbnailed input image
            palette: palette with custom colors to be used in the new image

        Returns:
            The recolored image
        """
        color_to_complete = 256 - len(palette)//3
        color1 = palette[:3]
        full_palette = palette + color1 * color_to_complete
        pal_img = Image.new("P", (1, 1))
        pal_img.putpalette(full_palette)

        return image.im.convert("P", 10, pal_img.im).convert("RGB")

    @staticmethod
    def base_plate_masking(value, target_color, actual_color, target_base_color):
        """ Thresholding colors for background color change applicable for round type lego bricks only

        Used in the PIL point function where color channels are shifted. If the color in the channel is 0,
        it is the base plate, so it is replaced by the base plate target color, otherwise it is the round type
        brick and changes the colors in each channels by shifting them compared to the target.

        Args:
            value: value in the channel coming from iterating lambda function
            actual_color: actual color of the lego brick in that channel
            target_color: target color of the lego brick in that channel
            target_base_color: target color for the base plate in the certain channel

        Returns:
            Returns either the base plate or the shifted color of the brick for the channel
        """
        if value == 0:
            return target_base_color
        else:
            return target_color - actual_color + value

    def colorize_brick(self, image, target_color, base_plate_color):
        """ Recoloring image by using the PIL point function for each of the channels

        With the point function the actual color of the brick/base plate is shifted compared to the target color
        in each channel. Finally the new, recolor image is reconstructed from the 3 modified channels.
        For further details pls check out the Pillow.point  documentation

        Args:
            image: thumbnailed input image
            target_color: color of the brick to be used
            base_plate_color: color of the base plate to be used

        Returns:
            The recolor image
        """
        bands = image.split()
        _r, _g, _b = target_color
        _r_base, _g_base, _b_base = base_plate_color

        if self.brick_type == "plate":
            r_offset = bands[0].point(lambda x: _r-115+x)
            g_offset = bands[1].point(lambda x: _g-115+x)
            b_offset = bands[2].point(lambda x: _b-115+x)
        elif self.brick_type == "round":
            r_offset = bands[0].point(lambda x: self.base_plate_masking(x, _r, 110, _r_base))
            g_offset = bands[1].point(lambda x: self.base_plate_masking(x, _g, 110, _g_base))
            b_offset = bands[2].point(lambda x: self.base_plate_masking(x, _b, 110, _b_base))
        elif self.brick_type == "tile":
            r_offset = bands[0].point(lambda x: _r-105+x)
            g_offset = bands[1].point(lambda x: _g-105+x)
            b_offset = bands[2].point(lambda x: _b-105+x)
        elif self.brick_type == "round tile":
            r_offset = bands[0].point(lambda x: self.base_plate_masking(x, _r, 110, _r_base))
            g_offset = bands[1].point(lambda x: self.base_plate_masking(x, _g, 110, _g_base))
            b_offset = bands[2].point(lambda x: self.base_plate_masking(x, _b, 110, _b_base))
        else:
            raise AttributeError("Non-valid brick type. You can choose plate, round, tile or round tile.")

        bands[0].paste(r_offset)
        bands[1].paste(g_offset)
        bands[2].paste(b_offset)

        return Image.merge(image.mode, bands)

    @staticmethod
    def count_bricks(img_small):
        """ This method counts bricks for each color that is used.

        Args:
            img_small: thumbnailed input image

        Returns:
            Number of bricks for each color used in a dict object
        """
        brick_rgb = [img_small.getpixel((w, h)) for w in range(img_small.size[0]) for h in range(img_small.size[1])]
        brick_hex = ['#{:02x}{:02x}{:02x}'.format(r, g, b) for r, g, b in brick_rgb]
        brick_id = [k for hexx in brick_hex for k, v in color_dict['hex'].items() if hexx == v]
        brick_name = [v for bid in brick_id for k, v in color_dict['lego_color'].items() if bid == k]
        color_count = {element: brick_name.count(element) for element in brick_name}

        return color_count

    def create_image(self, color_dictionary, base_plate_color):
        """ Main function creating legolized iamge

        Args:
            color_dictionary: dict with colors chosen by the user
            base_plate_color: color of the base plate chosen by the user

        Returns:
            No return value
        """
        self.brick_style()
        max_brick_size = (self.brick_size, self.brick_size)
        img_tranform = self.img.copy()
        img_tranform.thumbnail(max_brick_size, resample=Image.NEAREST)
        color_palette, color_nr = self.create_color_palette(color_dictionary)
        img_tranform = self.convert_color_matching(img_tranform, color_palette)
        # img_tranform = self.quantize_color_matching(img_tranform, color_palette, color_nr)
        self.brick_nr = self.count_bricks(img_tranform)

        brick_img_s, brick_nr_w, brick_nr_h = self.brick_sizer(img_tranform)
        self.brick_img = self.brick_img.resize((brick_img_s, brick_img_s), resample=Image.LINEAR)

        self.lego_image = Image.new('RGB', (brick_img_s * brick_nr_w, brick_img_s * brick_nr_h), "white")
        for w in range(brick_nr_w):
            for h in range(brick_nr_h):
                pixel_colors = img_tranform.getpixel((w, h))
                img_brick_single = self.colorize_brick(self.brick_img, pixel_colors, base_plate_color)
                self.lego_image.paste(img_brick_single, (w * brick_img_s, h * brick_img_s))

    def save_image(self, filename):
        """ Save image to a given location

        Args:
            filename: location where the final iamge is saved

        Returns:
            No returns
        """
        self.lego_image.save(filename)
