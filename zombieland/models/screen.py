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
	coordRoute = None
	cost = {(0,0): None}
	route = {(0,0): None}



	#screen cableado
	def __init__(self):
		for i in xrange (0, 15):
			for j in xrange(0, 21):
				self.pos[i,j]=tile(1,True)
		self.initRouteMap()
		self.cost[7,10]=0
		self.calculateCosts(7,10)
		self.route[7,10]=None


	#inicia la matriz de rutas con un costo de 1000 en cada cuadro
	def initRouteMap(self):
		for i in xrange (0, 15):
			for j in xrange(0, 21):
				self.cost[i,j]=1000
				self.route[i,j]=None

	#backtracking bitch!!
	def calculateCosts(self,i,j):
		if i < 14 and j < 20 and i > 0 and j > 0:
			for k in (-1,1):
				if self.cost[i,j]+1 < self.cost[i+k,j]:
					self.cost[i+k,j] = self.cost[i,j]+1
					self.route[i+k,j] = (i,j)
					self.calculateCosts(i+k,j)
				if self.cost[i,j]+1 < self.cost[i,j+k]:
					self.cost[i,j+k] = self.cost[i,j]+1
					self.route[i,j+k] = (i,j)
					self.calculateCosts(i,j+k)


	def getRoute(self,posy,posx,pposy,pposx):
		route = []
		posx += 1
		posy += 1
		print "move to:{} player coords: {}".format((posx,posy),(pposx,pposy))
		if self.route[posx,posy] != None:
			route.append((posy - 10 + pposy, 7 - posx + pposx))
			while (self.route[posx,posy] != (7,10)):
				auxPosx = self.route[posx,posy][0]
				auxPosy = self.route[posx,posy][1]
				posx=auxPosx
				posy=auxPosy
				route.append((posy - 10 +pposy,7 - posx + pposx))
		print route
		return route


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

