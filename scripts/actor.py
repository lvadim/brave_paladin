import pygame
from scripts import animated_sprite

class Actor:
	def __init__(self, logic, game, uid):
		self.sprite = animated_sprite.AnimatedSprite(self.onAnimationComplete)
		self.logic = logic
		self.logic.assignView(self.sprite)
		self.game = game
		self.uid = uid

	def draw(self):
		x, y = self.getSpriteActualPosition()
		self.sprite.SetPosition(x, y)
		self.sprite.Draw()
		
	def update(self):
		self.logic.Update()
		self.sprite.Update()

	def onAnimationComplete(self, name):
		self.logic.onAnimationComplete(name)

	def getSpriteActualPosition(self):
		w, h = self.sprite.GetSize()
		x, y = self.logic.GetPosition()
		mx, my = self.game.getMapPosition()
		return(mx + x - w / 2, my + y - h)

	def getY(self):
		return self.logic.pos_y

	def isRightDierction(self):
		return not self.sprite.need_flip

	def getPosition(self):
		return (self.logic.pos_x, self.logic.pos_y)
		
	def getAttackDist(self):
		return self.logic.attack_distance

	def onDamage(self, damage_count):
		self.logic.onDamage(damage_count)