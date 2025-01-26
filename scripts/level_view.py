import pygame
import numpy as np
from scripts import map_data
from scripts import level_generator
from scripts import game_screen
import math
import random

class Tileset:
    def __init__(self, map_info):
        self.file = map_info.image_file
        self.size = (map_info.tile_width, map_info.tile_height)
        self.margin = map_info.margin
        self.spacing = map_info.spacing
        self.image = pygame.image.load(map_info.image_file)
        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()

    def load(self):
        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing
        
        for y in range(y0, h, dy):
            for x in range(x0, w, dx):
                #tile = pygame.Surface(self.size)
                tile = pygame.Surface(self.size, pygame.SRCALPHA, 32)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'

class Tilemap:
    def __init__(self, tileset, map_info, level_generator = None): 
        self.size = (map_info.width, map_info.height)
        self.tileset = tileset
        self.tile_width = map_info.tile_width
        self.tile_height = map_info.tile_height
        self.map = np.full(self.size, fill_value = -1, dtype = int)
        self.passable = map_info.passable
        self.decor = map_info.decor
        self.objects = map_info.objects

        if level_generator:
            self.map = level_generator.GetLevelData()
        else:
            #print("---> shape:", len(map_info.tiles1), " ", len(map_info.tiles1[0]), " ", map_info.tiles1[0][0])
            for i in range(map_info.width):
                for j in range(map_info.height):
                    self.map[j, i] = map_info.tiles1[i][j]

        h, w = self.size
        #self.image = pygame.Surface((map_info.tile_width * w, map_info.tile_height * h)) #, pygame.SRCALPHA, 32)
        self.image = pygame.Surface((map_info.tile_width * w, map_info.tile_height * h), pygame.SRCALPHA, 32)
        #self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.render()

    def render(self):
        m, n = self.map.shape
        #print("--->shape : ", n, " ", m)
        for i in range(m):
            for j in range(n):
                tile_index = self.map[i, j]
                if(tile_index >= 0):
                    #print("---> tileset: ", len(self.tileset.tiles), " i:", self.map[i, j])
                    tile = self.tileset.tiles[self.map[i, j]]
                    self.image.blit(tile, (i * self.tile_width, j * self.tile_height))

        for decor in self.decor:
            x = decor['x']
            y = decor['y']
            tile = self.tileset.tiles[decor["tile"]]
            self.image.blit(tile, (x * self.tile_width, y * self.tile_height))

        for obj in self.objects:
            x = obj['x']
            y = obj['y']
            tile = self.tileset.tiles[obj["tile"]]
            self.image.blit(tile, (x * self.tile_width, y * self.tile_height))
            self.map[x, y] = 1000 # --- to avoid passable here

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'

class LevelView:
    def __init__(self, map_filename, level_generator = None):
        mapData = map_data.MapData(map_filename)
        tileset = Tileset(mapData)
        self.tilemap = Tilemap(tileset, mapData, level_generator)
        self.pos_x = 0
        self.pos_y = 0

    def draw(self):
        self.tilemap.rect.x = self.pos_x
        self.tilemap.rect.y = self.pos_y
        game_screen.Screen.screen.blit(self.tilemap.image, self.tilemap.rect)

    def SetPosition(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def move(self, dx, dy):
        self.pos_x += dx
        self.pos_y += dy

    def GetPosition(self):
        return (self.pos_x, self.pos_y)

    def getTileSize(self):
        return (self.tilemap.tile_width, self.tilemap.tile_height)

    def isPassable(self, x, y):
        cell_x, cell_y = self.getCellByCoord(x, y)
        w, h = self.tilemap.map.shape
        if cell_x < 0 or cell_y < 0 or cell_x >= w or cell_y >= h: return False
        return self.tilemap.map[cell_x, cell_y] in self.tilemap.passable

    def getCellByCoord(self, x, y):
        cell_x = math.floor(x / self.tilemap.tile_width)
        cell_y = math.floor(y / self.tilemap.tile_height)
        return (cell_x, cell_y)  

    def getCellCoordinates(self, cell_x, cell_y):
        x = cell_x * self.tilemap.tile_width + self.tilemap.tile_width / 2
        y = cell_y * self.tilemap.tile_height + self.tilemap.tile_height / 2
        return (x, y)

    def getRandomPassableCoord(self):
        m, n = self.tilemap.map.shape
        results = []
        for i in range(m):
            for j in range(n):
                if self.tilemap.map[i, j] in self.tilemap.passable:
                    results.append((i, j))

        result_x, result_y = random.choice(results)
        return self.getCellCoordinates(result_x, result_y)

    def reloadMap(self, map_filename):
        mapData = map_data.MapData(map_filename)
        tileset = Tileset(mapData)
        self.tilemap = Tilemap(tileset, mapData, None)
        