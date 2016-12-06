import pygame, sys
import time 
import threading
import json
from player import *
from pygame.locals import *
from random import randint
from tile import *
from decimal import Decimal
#Tamano de sqm
SQM_SIZE=32
#cantidad de cuadros en el scrin +1 adicional a cada lado
SCREEN_WIDTH = 21
SCREEN_HEIGHT = 15
POS_INF = Decimal ('Infinity')
NEG_INF = Decimal ('-Infinity')


#Clase screen
class screen():
	#Desplazamiento para desplazar el fondo a medida q se mueve el jugador
	displacementX=0
	displacementY=0

	file = open('maps/map', 'r')
	map=json.load(file)
	pos = {(0,0): None}
	coordRoute = None
	cost = {(0,0): None}
	route = {(0,0): None}
	test =1

	#screen cableado, genera un minimapa de 15 x 21 cuadros, con solo piso tipo 1 sin ningun tipo de obstaculo
	#todos los tiles son caminables
	def __init__(self,posx,posy):
		for y in xrange (-(SCREEN_HEIGHT/2+1)+posy, (SCREEN_HEIGHT/2+1)+posy+1):
			for x in xrange(-(SCREEN_WIDTH/2+1)+posx, (SCREEN_WIDTH/2+1)+posx+1):
				if self.map[str(x)+','+str(y)]=='walkable':
					self.pos[x,y]=tile(self.map[str(x)+','+str(y)],True)
					self.cost[x, y] = POS_INF
				else:
					self.pos[x, y] = tile(self.map[str(x)+','+str(y)], False)
					self.cost[x, y] = None
				self.route[x, y] = None

		#asigna el costo 0 a la posicion donde se encuentra parado el jugador
		self.cost[posx,posy]=0
		#calcula los costos con backtracking explorando toda la matriz
		self.calculateCosts(posx,posy,posx,posy)
		#asigna None a la posicion de la matriz route donde se encuentra nuestro jugador (esta instruccion creo q no es necesaria)
		self.route[posx,posy]=None

	def expandTop(self, posx, posy):
		y= (SCREEN_HEIGHT / 2 + 1) + posy
		for x in xrange(-(SCREEN_WIDTH / 2 + 1) + posx, (SCREEN_WIDTH / 2 + 1) + posx + 1):
			if self.map[str(x) + ',' + str(y)] == 'walkable':
				self.pos[x, y] = tile(self.map[str(x) + ',' + str(y)], True)
			else:
				self.pos[x, y] = tile(self.map[str(x) + ',' + str(y)], False)

	def getCost(self,posx,posy):
		print "getting cost with", posx, posy
		self.cost = {(0, 0): None}
		print "cost matrix is clear"
		self.route = {(0, 0): None}
		print "route matrix is clear"
		for y in xrange(-(SCREEN_HEIGHT / 2 + 1) + posy, (SCREEN_HEIGHT / 2 + 1) + posy + 1):
			for x in xrange(-(SCREEN_WIDTH / 2 + 1) + posx, (SCREEN_WIDTH / 2 + 1) + posx + 1):
				if self.map[str(x) + ',' + str(y)] == 'walkable':
					self.cost[x, y] = POS_INF
				else:
					self.cost[x, y] = None
				self.route[x, y] = None
		self.cost[posx, posy] = 0
		self.route[posx, posy] = None
		print "cost and route setting is done"

	def expandDown(self, posx, posy):
		y = posy-(SCREEN_HEIGHT/2+1)
		for x in xrange(-(SCREEN_WIDTH / 2 + 1) + posx, (SCREEN_WIDTH / 2 + 1) + posx + 1):
			if self.map[str(x) + ',' + str(y)] == 'walkable':
				self.pos[x, y] = tile(self.map[str(x) + ',' + str(y)], True)
			else:
				self.pos[x, y] = tile(self.map[str(x) + ',' + str(y)], False)

	def expandLeft(self, posx, posy):
		x= posx-(SCREEN_WIDTH / 2 + 1)
		for y in xrange(-(SCREEN_HEIGHT / 2 + 1) + posy, (SCREEN_HEIGHT / 2 + 1) + posy + 1):
			if self.map[str(x) + ',' + str(y)] == 'walkable':
				self.pos[x, y] = tile(self.map[str(x) + ',' + str(y)], True)
			else:
				self.pos[x, y] = tile(self.map[str(x) + ',' + str(y)], False)

	def expandRight(self, posx, posy):
		x = (SCREEN_WIDTH / 2 + 1) + posx
		for y in xrange(-(SCREEN_HEIGHT / 2 + 1) + posy, (SCREEN_HEIGHT / 2 + 1) + posy + 1):
			if self.map[str(x) + ',' + str(y)] == 'walkable':
				self.pos[x, y] = tile(self.map[str(x) + ',' + str(y)], True)
			else:
				self.pos[x, y] = tile(self.map[str(x) + ',' + str(y)], False)

	def reCalculate(self, posx, posy):
		self.getCost(posx, posy)
		print "calculating costs"
		self.calculateCosts(posx, posy, posx, posy)
		print "cost are calculated"

	#Exploracion de matriz de costos con backtracking bitch!!
	#no se exploran tiles no caminables
	def calculateCosts(self,i,j,posx,posy):
		limxLeft= posx-(SCREEN_WIDTH/2)
		limxRight=posx+(SCREEN_WIDTH/2)
		limyDown=posy-(SCREEN_HEIGHT/2)
		limyTop=posy+(SCREEN_HEIGHT/2)

		#verificacion de limite del screen
		if i < limxRight and j < limyTop and i > limxLeft and j > limyDown:
			for k in (-1,1):
				if self.cost[i+k,j] != None:
					if self.cost[i,j]+1 < self.cost[i+k,j]:
						self.cost[i+k,j] = self.cost[i,j]+1
						self.route[i+k,j] = (i,j)
						self.calculateCosts(i+k,j,posx,posy) #llamada recursiva
				if self.cost[i, j+k] != None:
					if self.cost[i,j]+1 < self.cost[i,j+k]:
						self.cost[i,j+k] = self.cost[i,j]+1
						self.route[i,j+k] = (i,j)
						self.calculateCosts(i,j+k,posx,posy) #llamada recursiva

	#Obtiene la ruta desde una posicion (pposy,pposx) hasta (posy,posx)
	def getRoute(self,posx,posy,pposx,pposy):
		#reinicio la ruta para borrar cualquier ruta previamente calculada
		route = []

		#si la posicion es alcanzable
		if self.route[posx,posy] != None:
			#se agrega el movimiento a la ruta
			route.append((posx, posy))
			#Mientras la posicion sea diferente de donde esta parado el jugador
			while (self.route[posx,posy] != (pposx,pposy)):
				auxPosx = self.route[posx,posy][0]
				auxPosy = self.route[posx,posy][1]
				posx=auxPosx
				posy=auxPosy
				#anadir a la lista el movimiento a realizar
				route.append((posx,posy))

		#retorna la lista en orden inverso de las coordenadas a las cual moverse para usarse con .pop()
		return route


	#funcion para realizar el movimiento del screen
	def move(self, mutex, dir, player,):
		if dir == "down":
			threading.Thread(target=self.reCalculate, args=(player.posx, player.posy-1,)).start()
			for i in xrange (1,SQM_SIZE):
				time.sleep(1.0/float(SQM_SIZE))
				self.displacementY -= 1
			mutex.acquire()
			self.displacementY = 0
			self.expandDown(player.posx,player.posy)
			player.posy -= 1
			mutex.release()

		elif dir == "up":
			threading.Thread(target=self.reCalculate, args=(player.posx, player.posy+1,)).start()
			for i in xrange (1,SQM_SIZE):
				time.sleep(1.0/float(SQM_SIZE))
				self.displacementY += 1
			mutex.acquire()
			self.displacementY = 0
			self.expandTop(player.posx, player.posy)
			player.posy += 1
			mutex.release()

		elif dir == "left":
			threading.Thread(target=self.reCalculate, args=(player.posx+1, player.posy,)).start()
			for i in xrange (1,SQM_SIZE):
				time.sleep(1.0/float(SQM_SIZE))
				self.displacementX += 1
			mutex.acquire()
			self.displacementX = 0
			self.expandLeft(player.posx, player.posy)
			player.posx -= 1
			mutex.release()

		elif dir == "right":
			threading.Thread(target=self.reCalculate, args=(player.posx-1, player.posy,)).start()
			for i in xrange (1,SQM_SIZE):
				time.sleep(1.0/float(SQM_SIZE))
				self.displacementX -= 1
			mutex.acquire()
			self.displacementX = 0
			self.expandRight(player.posx, player.posy)
			player.posx += 1
			mutex.release()
		player.status = "waiting"





