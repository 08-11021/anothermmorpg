from player import *

#Clase para los cuadros del piso
class tile(pygame.sprite.Sprite):
	background="" #recurso para el piso
	objects=[] #objetos contenidos en el cuadro
	player=None #id del player ubicado en el cuadro
	walkable=True #si es caminable o no el cuadro

	def __init__(self,ground, walkable):
		pygame.sprite.Sprite.__init__(self)
		self.background = pygame.image.load("../tiles/"+ground+".png")
		self.walkable = walkable

	def isWalkable(self):
		return self.walkable

	def addObject(self, object):
		self.objects.append(object)

	def removeObject(self, object):
		try:
			self.objects.pop()
		except:
			self.objects = self.objects

	def addPlayer(self, player):
		self.player= player