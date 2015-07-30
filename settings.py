"""Common settings for application and testing"""
import pickle
from Queue import Queue

# measurements in feet
bot_height = 0.323
bot_radius = 0.35
maze_width = 9.0
maze_length = 15.0

image_height = 600
maze = {}
bot = {}

raw_image = []
map_image = []

maze = {}
bot_front = {}
bot_back = {}
overlay = {}

track_bot = False
robo_go = False
camera_height = 5.0
camera_distance = 7.0

bot_position = (100, 100)
goal_position = (200, 200)
running = True

path_finder_max_img_height = 500
path_finder_max_img_width = 500

path_q = Queue()


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


def save(path='settings.pyb'):
    output = open(path, 'wb')
    print "Saving settings to " + path
    pickle.dump(top_left, output)
    pickle.dump(top_right, output)
    pickle.dump(bottom_right, output)
    pickle.dump(bottom_left, output)
    pickle.dump(camera_height, output)
    pickle.dump(camera_distance, output)
    for purpose in maze, bot_front, bot_back, overlay:
        pickle.dump(purpose['ey'], output)
        pickle.dump(purpose['ex'], output)
        pickle.dump(purpose['dy'], output)
        pickle.dump(purpose['dx'], output)
        pickle.dump(purpose['hMin'], output)
        pickle.dump(purpose['hMax'], output)
        pickle.dump(purpose['sMin'], output)
        pickle.dump(purpose['sMax'], output)
        pickle.dump(purpose['vMin'], output)
        pickle.dump(purpose['vMax'], output)
    output.close()
    print "Save complete"


def load(path='settings.txt'):
    input = open(path, 'r')
    print "Loading settings from " + path
    global top_left
    global top_right
    global bottom_right
    global bottom_left
    global camera_height
    global camera_distance
    global maze
    global bot_front
    global bot_back
    global overlay
    top_left = pickle.load(input)
    top_right = pickle.load(input)
    bottom_right = pickle.load(input)
    bottom_left = pickle.load(input)
    camera_height = pickle.load(input)
    camera_distance = pickle.load(input)
    for purpose in maze, bot_front, bot_back, overlay:
        purpose['ey'] = pickle.load(input)
        purpose['ex'] = pickle.load(input)
        purpose['dy'] = pickle.load(input)
        purpose['dx'] = pickle.load(input)
        purpose['hMin'] = pickle.load(input)
        purpose['hMax'] = pickle.load(input)
        purpose['sMin'] = pickle.load(input)
        purpose['sMax'] = pickle.load(input)
        purpose['vMin'] = pickle.load(input)
        purpose['vMax'] = pickle.load(input)
    input.close()
    print "Load Complete"

