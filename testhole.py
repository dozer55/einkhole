#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import json
import urllib2
path = "/home/pi/piholdDisp"
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    f = urllib2.urlopen('http://192.168.1.68/admin/api.php')
    w = urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?q=Chattanooga,TN,US&appid=d569bfbc7253c3a19356ee57b53e9881&units=Imperial')
    wjson_string = w.read()
    wparsed_json = json.loads(wjson_string)
    temp = wparsed_json['main']['temp']
    json_string = f.read()
    parsed_json = json.loads(json_string)
    adsblocked = parsed_json['ads_blocked_today']
    ratioblocked = parsed_json['ads_percentage_today']
    status = parsed_json['status']
    logging.info("epd2in13_V2 Demo")   
    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    logging.info("Ads Blocked: " + str(adsblocked))
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    # Drawing on the image
    font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    
    logging.info("1.Drawing on the image...")
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)
    draw.text((0,0), 'Pi Hole Stats', font = font24, fill = 0) 
    draw.text((0,22), 'Ads Blocked: ' + str(adsblocked), font = font20)
    draw.text((0,40), 'Ads %: ' + str(ratioblocked), font = font20, fill = 0)
    draw.text((0,58), 'Status: ' + str(status), font = font20, fill=0)
    draw.text((0,90), 'Current Temp: ' + str(temp), font = font20, fill=0)
    epd.display(epd.getbuffer(image))
    time.sleep(2)

    
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
