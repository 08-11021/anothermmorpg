import pygame, sys
import time 
import threading
from pygame.locals import *
from random import randint
from tile import *

#Tamano de sqm
SQM_SIZE=32

#Clase screen
class screen():
	#Desplazamiento para desplazar el fondo a medida q se mueve el jugador
	displacementX=0
	displacementY=0

	pos = {(0,0): None}
	coordRoute = None
	cost = {(0,0): None}
	route = {(0,0): None}

	#screen cableado, genera un minimapa de 15 x 21 cuadros, con solo piso tipo 1 sin ningun tipo de obstaculo
	#todos los tiles son caminables
	def __init__(self):
		for i in xrange (0, 15):
			for j in xrange(0, 21):
				self.pos[i,j]=tile(1,True)

		#inicializa la matriz cost con el valor 1000 en cada elemento (costo)
		#y None en los elementos de la matriz route
		self.initRouteMap()
		#asigna el costo 0 a la posicion donde se encuentra parado el jugador
		self.cost[7,10]=0
		#calcula los costos con backtracking explorando toda la matriz
		self.calculateCosts(7,10)
		#asigna None a la posicion de la matriz route donde se encuentra nuestro jugador (esta instruccion creo q no es necesaria)
		self.route[7,10]=None


	#inicia la matriz de costos con un costo de 1000 en cada cuadro
	#inicia la matriz de rutas con None en cada cuadro
	def initRouteMap(self):
		for i in xrange (0, 15):
			for j in xrange(0, 21):
				self.cost[i,j]=1000
				self.route[i,j]=None

	#Exploracion de matriz de costos con backtracking bitch!!
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

	#Obtiene la ruta desde una posicion (pposy,pposx) hasta (posy,posx)
	def getRoute(self,posy,posx,pposy,pposx):
		#reinicio la ruta para borrar cualquier ruta previamente calculada
		route = []
		#sumo 1 a las posiciones x e y porque hay un cuadro adicional en todos los extremos del screen
		posx += 1
		posy += 1

		#si la posicion es alcanzable
		if self.route[posx,posy] != None:
			#se agrega el movimiento a la ruta
			route.append((posy - 10 + pposy, 7 - posx + pposx))
			#Mientras la posicion sea diferente de donde esta parado el jugador
			while (self.route[posx,posy] != (7,10)):
				auxPosx = self.route[posx,posy][0]
				auxPosy = self.route[posx,posy][1]
				posx=auxPosx
				posy=auxPosy
				#anadir a la lista el movimiento a realizar
				route.append((posy - 10 +pposy,7 - posx + pposx))

		#retorna la lista en orden inverso de las coordenadas a las cual moverse para usarse con .pop()
		return route

	#funcion para realizar el movimiento del screen
	def move(self, dir):
		if dir == "down":
			for i in xrange (1,SQM_SIZE):
				time.sleep(1.0/float(SQM_SIZE))
				self.displacementY -= 1
			#en este punto hay q actualizar el contenido del mapa para esto hay q descablear el screen
			self.displacementY = 0
		elif dir == "up":
			for i in xrange (1,SQM_SIZE):
				time.sleep(1.0/float(SQM_SIZE))
				self.displacementY += 1
			# en este punto hay q actualizar el contenido del mapa para esto hay q descablear el screen
			self.displacementY = 0
		elif dir == "left":
			for i in xrange (1,SQM_SIZE):
				time.sleep(1.0/float(SQM_SIZE))
				self.displacementX += 1
			# en este punto hay q actualizar el contenido del mapa para esto hay q descablear el screen
			self.displacementX = 0
		elif dir == "right":
			for i in xrange (1,SQM_SIZE):
				time.sleep(1.0/float(SQM_SIZE))
				self.displacementX -= 1
			# en este punto hay q actualizar el contenido del mapa para esto hay q descablear el screen
			self.displacementX = 0

