import json

class MapData:
    def __init__(self, filename):
    	self.load(filename)

    def load(self, filename):
        f = open(filename)
        data = json.load(f)
        self.width = data["width"]
        self.height = data["height"]
        self.tile_width = data["source"]['tile_width']
        self.tile_height = data["source"]['tile_height']
        self.verticals = data["source"]['verticals']
        self.horizontals = data["source"]['horizontals']
        self.image_file = data["source"]['image']
        self.margin = data["source"]['margin']
        self.spacing = data["source"]['spacing']

        self.tiles = data['tiles']
        self.tiles1 = data['tiles1']
        self.passable = data['passable']
        self.decor = data['decor']
        self.objects = data['objects']