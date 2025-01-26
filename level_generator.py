import numpy as np
import random

class LevelGenerator:
	def __init__(self):
	 	{}

	def GetLevelData(self):
		s = (10, 10)
		#level = np.full(self.size, fill_value = -1, dtype = int)
		#level = np.random.randint(2, size = s)
		level = np.full(s, fill_value = -1, dtype = int)

		# --- 1 room -----------------------------------------
		# --- top
		for x in range(0, 10):
			level[x, 0] = random.randrange(17, 20)

		for x in range(0, 10):
			level[x, 1] = random.randrange(21, 24)
		
		level[0, 0] = 16
		level[0, 1] = 20

		#--- walkable place
		for x in range(0, 10):
			level[x, 9] = random.randrange(13, 15)

		for x in range(0, 10):
			for y in range(3, 9):
				level[x, y] = random.randrange(5, 9)

		#--- break
		for x in range(0, 10):
			level[x, 9] = random.randrange(13, 15)

		return level