"""Common settings for application and testing"""
import numpy as np

class Settings():
    def __init__(self):
        self.image_height = 600

        #Defaults for map
        self.ey   =  1
        self.ex   =  1
        self.dy   =  1
        self.dx   =  1
        self.rMin =  0
        self.rMax =  255
        self.gMin =  0
        self.gMax =  255
        self.bMin =  100
        self.bMax =  255
        self.top_left = (195, 53)
        self.top_right = (416, 54)
        self.bottom_right = (585, 312)
        self.bottom_left = (23, 316)

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, item, value):
        self.__dict__[item] = value

settings = Settings()
