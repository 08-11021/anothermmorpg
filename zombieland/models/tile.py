import pygame, sys
import time 
import threading
from pygame.locals import *
from random import randint
from player import *

class tile(pygame.sprite.Sprite):
	"""clase para zombies"""
	background=""
	objects=[]
	player=None
	walkable=True

	def __init__(self,ground, walkable):
		pygame.sprite.Sprite.__init__(self)
		self.background = pygame.image.load("../tiles/"+str(ground)+".png")
		self.walkable = walkable


	def addObject(self, object):
		self.objects.append(object)

	def removeObject(self, object):
		try:
			self.objects.pop()
		except:
			self.objects = self.objects

	def addPlayer(self, player):
		self.player= player