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
		self.cost[7,9]=0
		self.calculateCosts(7,9)
		self.route[7,9]=None
		for i in xrange (0, 15):
				print '{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}'.format(self.cost[i,0],self.cost[i,1],self.cost[i,2],self.cost[i,3],self.cost[i,4],self.cost[i,5],self.cost[i,6],self.cost[i,7],self.cost[i,8],self.cost[i,9],self.cost[i,10],self.cost[i,11],self.cost[i,12],self.cost[i,13],self.cost[i,14],self.cost[i,i],self.cost[i,16],self.cost[i,17],self.cost[i,18])

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

	def getRoute(self,posy,posx):
		route = []

		while (self.route[posx,posy] != None):
			print 'start'
			print self.route[posx,posy]
			posx = self.route[posx,posy][0]
			posy = self.route[posx,posy][1]
			route.append((posx,posy))
			print(posx,posy)
		print route


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

