import pygame
import animated_sprite

class Actor:
	def __init__(self, logic, data_provider, uid):
		self.sprite = animated_sprite.AnimatedSprite(self.onAnimationComplete)
		self.logic = logic
		self.logic.assignView(self.sprite)
		self.data_provider = data_provider
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
		mx, my = self.data_provider.getMapPosition()
		return(mx + x - w / 2, my + y - h)

	def getY(self):
		return self.logic.pos_y

	def isRightDierction(self):
		return not self.sprite.need_flip

	def getPosition(self):
		return (self.logic.pos_x, self.logic.pos_y)
		
	def getAttackDist(self):
		return self.logic.attackDist

	def onDamage(self, damage_count):
		self.logic.onDamage(damage_count)