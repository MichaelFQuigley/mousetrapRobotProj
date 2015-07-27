"""Common settings for application and testing"""
import numpy as np

image_height = 600
maze = {}
bot = {}

raw_image = []

#defaults for map
maze['ey'] = 1
maze['ex'] = 1
maze['dy'] = 1
maze['dx'] = 1
maze['hMin'] = 0
maze['hMax'] = 255
maze['sMin'] = 0
maze['sMax'] = 255
maze['vMin'] = 100
maze['vMax'] = 255
maze['top_left'] = (195, 53)
maze['top_right'] = (416, 54)
maze['bottom_right'] = (585, 312)
maze['bottom_left'] = (23, 316)

#defaults for bot
bot['bot_position'] = (0, 0)
bot['goal_position'] = (1, 1)
bot['ey'] = 1
bot['ex'] = 1
bot['dy'] = 1
bot['dx'] = 1
bot['hMin'] = 0
bot['hMax'] = 255
bot['sMin'] = 0
bot['sMax'] = 255
bot['vMin'] = 100
bot['vMax'] = 255
bot['top_left'] = (195, 53)
bot['top_right'] = (416, 54)
bot['bottom_right'] = (585, 312)
bot['bottom_left'] = (23, 316)

def get_map(name):
    return maze if name == 'maze' else bot