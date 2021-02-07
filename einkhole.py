#!/usr/bin/python
# -*- coding:utf-8 -*-

# Import Packages (make sure these are installed!!! pip is your friend!)

import sys
import os
import json
import urllib2
import yaml

# Grab config from config.yml (make sure you edit config.yml with your specifics)


with open("config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)
for section in cfg:
    source = cfg["paths"]["url"]
    path = cfg["paths"]["home"]

# defines paths to resources
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')

if os.path.exists(libdir):
    sys.path.append(libdir)

# set up waveshare stuff for display output
import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

# Now the fun begins! Let's display some stuff!!!
try:
    # Open pihole json stats source and load into variables
    f = urllib2.urlopen(source)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    adsblocked = parsed_json['ads_blocked_today']
    ratioblocked = parsed_json['ads_percentage_today']
    status = parsed_json['status']
    
    # Initialize e-ink display
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    # Clear anything existing on the display
    epd.Clear(0xFF)
    
    # Define fonts to be used
    font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    
    # Write to display
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)
    draw.text((0,0), 'Pi Hole Stats', font = font24, fill = 0) 
    draw.text((0,22), 'Ads Blocked: ' + str(adsblocked), font = font20)
    draw.text((0,40), 'Ads %: ' + str(ratioblocked), font = font20, fill = 0)
    draw.text((0,58), 'Status: ' + str(status), font = font20, fill=0)
    epd.display(epd.getbuffer(image))
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
