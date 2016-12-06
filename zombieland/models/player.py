import pygame, sys
import time 
import threading
from pygame.locals import *
from random import randint

#Clase player
class player(pygame.sprite.Sprite):
	posx=0
	posy=0
	outfit="GM"
	speed = 2
	lvl=1
	status = "waiting"
	outfits=["coctelero","machetero","escopetero","doctor","GM"] #Nombres dummy de los outfit pertenecientes a cada clase

	#Init de la clase player, se usa el sprite viendo hacia abajo que esta detenido
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.ImagePlayer = pygame.image.load("../outfits/"+self.outfit+"/down/2.png")

	#Metodo walk del personaje
	def walk(self, dir):
		self.status="walking"
		self.ImagePlayer = pygame.image.load("../outfits/"+self.outfit+"/"+dir+"/1.png")
		time.sleep(1.0/3.0)
		self.ImagePlayer = pygame.image.load("../outfits/"+self.outfit+"/"+dir+"/2.png")
		time.sleep(1.0/3.0)
		self.ImagePlayer = pygame.image.load("../outfits/"+self.outfit+"/"+dir+"/3.png")
		time.sleep(1.0/3.0)
		self.ImagePlayer = pygame.image.load("../outfits/"+self.outfit+"/"+dir+"/2.png")

		print(self.posx,self.posy)

	#Metodo para cambiar outfit del jugador
	def nextOutfit(self):
		self.outfit= self.outfits.pop(0)
		self.outfits.append(self.outfit)
		print "outfit changed: "+self.outfit
