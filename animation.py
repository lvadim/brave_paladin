import json

class AnimationData:
    def __init__(self, filename):
        self.load(filename)

    def load(self, filename):
        f = open(filename)
        data = json.load(f)
        self.width = data['width']
        self.height = data['height']
        self.image_file = data['image_file']
        self.animation_speed = data['animation_speed']
        self.frames = data['frames']
        self.name = data['name']


class Animation:
    def __init__(self, sprites, animatiom_data):
        self.sprites = sprites
        self.speed = animatiom_data.animation_speed
        self.width = animatiom_data.width
        self.height = animatiom_data.height
        self.name = animatiom_data.name