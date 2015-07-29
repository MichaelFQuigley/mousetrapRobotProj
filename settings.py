"""Common settings for application and testing"""
import numpy as np

# measurements in feet
bot_height = 0.323
bot_radius = 0.35
maze_width = 9.0
maze_length = 14.0

image_height = 600
maze = {}
bot = {}

raw_image = []
map_image = []

maze = {}
bot_front = {}
bot_back= {}
overlay = {}

track_bot = False
camera_height = 1.0
camera_distance = 1.0

for a_set in maze, bot_front, bot_back, overlay:
    a_set['ey'] = 1
    a_set['ex'] = 1
    a_set['dy'] = 1
    a_set['dx'] = 1
    a_set['hMin'] = 0
    a_set['hMax'] = 255
    a_set['sMin'] = 0
    a_set['sMax'] = 255
    a_set['vMin'] = 100
    a_set['vMax'] = 255
    a_set['image'] = None

top_left = (195, 53)
top_right = (416, 54)
bottom_right = (585, 312)
bottom_left = (23, 316)


def get_map(name):
    purposes = {
        'overlay': overlay,
        'bot_front': bot_front,
        'bot_back': bot_back,
        'maze': maze
    }
    return purposes[name]
