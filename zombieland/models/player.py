#ROJO,VERDE,AZUL

import pygame, sys
import time 
import threading
from pygame.locals import *
from random import randint

class player(pygame.sprite.Sprite):
	"""clase para zombies"""
	posx=0
	posy=0
	outfit="GM"
	speed = 2
	status = "waiting"
	outfits=["coctelero","machetero","escopetero","doctor","GM"]

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.ImagePlayer = pygame.image.load("../outfits/"+self.outfit+"/down/2.png")



		self.Vida = 300

	def walk(self, dir):
		self.status="walking"
		self.ImagePlayer = pygame.image.load("../outfits/"+self.outfit+"/"+dir+"/1.png")
		time.sleep(1.0/3.0)
		self.ImagePlayer = pygame.image.load("../outfits/"+self.outfit+"/"+dir+"/2.png")
		time.sleep(1.0/3.0)
		self.ImagePlayer = pygame.image.load("../outfits/"+self.outfit+"/"+dir+"/3.png")
		time.sleep(1.0/3.0)
		self.ImagePlayer = pygame.image.load("../outfits/"+self.outfit+"/"+dir+"/2.png")
		if dir == "down":
			self.posy -= 1
		elif dir == "up":
			self.posy += 1
		elif dir == "left":
			self.posx -= 1
		elif dir == "right":
			self.posx += 1 
		self.status="waiting"
		print(self.posx,self.posy)

	def nextOutfit(self):
		self.outfit= self.outfits.pop(0)
		self.outfits.append(self.outfit)
		print "outfit changed: "+self.outfit
