"""Common settings for application and testing"""
import numpy as np

image_height = 600
maze = {}
bot = {}

#defaults for map
maze['ey'] = 1
maze['ex'] = 1
maze['dy'] = 1
maze['dx'] = 1
maze['rMin'] = 0
maze['rMax'] = 255
maze['gMin'] = 0
maze['gMax'] = 255
maze['bMin'] = 100
maze['bMax'] = 255
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
bot['rMin'] = 0
bot['rMax'] = 255
bot['gMin'] = 0
bot['gMax'] = 255
bot['bMin'] = 100
bot['bMax'] = 255

def get_map(name):
    return maze if name == 'maze' else bot