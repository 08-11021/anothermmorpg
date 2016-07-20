#ROJO,VERDE,AZUL

import pygame, sys
import time 
import threading
from pygame.locals import *
from random import randint
from tile import *

class screen():
	"""clase para screen"""
	displacementX=0
	displacementY=0
	pos = {(0,0): None}

	def __init__(self):
		for i in xrange (0, 15):
			for j in xrange(0, 21):
				self.pos[i,j]=tile(1,True)

	def move(self, dir):
		if dir == "down":
			for i in xrange (1,32):
				time.sleep(1.0/32.0)
				self.displacementY -= 1
			self.displacementY = 0
		elif dir == "up":
			for i in xrange (1,32):
				time.sleep(1.0/32.0)
				self.displacementY += 1
			self.displacementY = 0
		elif dir == "left":
			for i in xrange (1,32):
				time.sleep(1.0/32.0)
				self.displacementX += 1
			self.displacementX = 0
		elif dir == "right":
			for i in xrange (1,32):
				time.sleep(1.0/32.0)
				self.displacementX -= 1 
			self.displacementX = 0

