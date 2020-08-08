#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import time
import argparse
import os
from PIL import Image, ImageDraw, ImageFont

inky_displayWHITE = 0
inky_displayBLACK = 1
inky_displayRED = inky_displayYELLOW = 2

# Get the current path

PATH = os.path.dirname(__file__)

def create_mask(source, mask=(inky_displayWHITE, inky_displayBLACK, inky_displayRED)):
    """Create a transparency mask.

    Takes a paletized source image and converts it into a mask
    permitting all the colours supported by Inky pHAT (0, 1, 2)
    or an optional list of allowed colours.

    :param mask: Optional list of Inky pHAT colours to allow.

    """
    mask_image = Image.new("1", source.size)
    w, h = source.size
    for x in range(w):
        for y in range(h):
            p = source.getpixel((x, y))
            if p in mask:
                mask_image.putpixel((x, y), 255)
    print(mask_image.getcolors())
    return mask_image


# Dictionaries to store our icons and icon masks in
icons = {}
masks = {}

# This maps the weather summary from Dark Sky
# to the appropriate weather icons
icon_map = {
    "snow": ["snow", "sleet"],
    "rain": ["rain"],
    "cloud": ["fog", "cloudy", "partly-cloudy-day", "partly-cloudy-night"],
    "sun": ["clear-day", "clear-night"],
    "storm": [],
    "wind": ["wind"]
}

# Placeholder variables
pressure = 0
temperature = 0
weather_icon = None

# Load our icon files and generate masks
for icon in glob.glob(os.path.join(PATH, "resources/icon-*.png")):
    icon_name = icon.split("icon-")[1].replace(".png", "")
    icon_image = Image.open(icon)
    icons[icon_name] = icon_image
    masks[icon_name] = create_mask(icon_image)

