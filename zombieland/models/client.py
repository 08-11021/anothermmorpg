# ROJO,VERDE,AZUL

import pygame, sys
import time
import threading
from pygame.locals import *
from random import randint
from player import *
from screen import *
from tile import *

# tam ventana
ancho = 608
alto = 416

map = []
routeMap = []


def dibujar(ventana, player, screen):
	for i in xrange(0, 15):
		posI = i * 32
		for j in range(0, 21):
			posJ = j * 32
			ventana.blit(screen.pos[i, j].background,
						 (posJ - 32 + screen.displacementX, posI - 32 + screen.displacementY))
	ventana.blit(player.ImagePlayer, (posX, posY))
	pygame.display.update()


def getRoute(coordx, coordy):
	# retorna una lista con el camino minimo desde la posicion del jugador hasta la coordenada x,y recibidas como parametro
	route = []
	explore(player.posx, player.posy)

	return route


pygame.init()
ventana = pygame.display.set_mode((ancho, alto))
screen = screen()
pygame.display.set_caption("ZombieLand")
player = player()
ruta = []
# miFuente = pygame.font.Font("mifuente.otf")
# miTexto = miFuente.render("prueba fuente",0,(200,60,80))
# ventana.blit(miFuente, (posX,posY))
posY, posX = (alto / 2) - 16, (ancho / 2) - 16
flagLeft = False
flagRight = False
flagUp = False
flagDown = False

while True:

	threading.Thread(target=dibujar, args=(ventana, player, screen,)).start()
	for evento in pygame.event.get():
		if evento.type == QUIT:
			pygame.quit()
			sys.exit()
		elif evento.type == pygame.KEYDOWN:
			if evento.key == K_LEFT:
				ruta = []
				flagLeft = True
			elif evento.key == K_RIGHT:
				ruta = []
				flagRight = True
			elif evento.key == K_UP:
				ruta = []
				flagUp = True
			elif evento.key == K_DOWN:
				ruta = []
				flagDown = True
			elif evento.key == K_c:
				threading.Thread(target=player.nextOutfit).start()
		elif evento.type == pygame.KEYUP:
			if evento.key == K_LEFT:
				flagLeft = False
			elif evento.key == K_RIGHT:
				flagRight = False
			elif evento.key == K_UP:
				flagUp = False
			elif evento.key == K_DOWN:
				flagDown = False
		elif evento.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[0] == 1:
				ruta = screen.getRoute(pygame.mouse.get_pos()[0] / 32, pygame.mouse.get_pos()[1] / 32, player.posx,
									   player.posy)

	if flagLeft:
		if player.status == "waiting":
			threading.Thread(target=player.walk, args=("left",)).start()
			threading.Thread(target=screen.move, args=("left",)).start()
	elif flagRight:
		if player.status == "waiting":
			threading.Thread(target=player.walk, args=("right",)).start()
			threading.Thread(target=screen.move, args=("right",)).start()
	elif flagUp:
		if player.status == "waiting":
			threading.Thread(target=player.walk, args=("up",)).start()
			threading.Thread(target=screen.move, args=("up",)).start()
	elif flagDown:
		if player.status == "waiting":
			threading.Thread(target=player.walk, args=("down",)).start()
			threading.Thread(target=screen.move, args=("down",)).start()
	elif ruta != []:
		if player.status == "waiting":
			coord= ruta.pop()
			direction = None

			if player.posx > coord[0]:
				direction = "left"
			elif player.posx < coord[0]:
				direction = "right"
			elif player.posy < coord[1]:
				direction = "up"
			elif player.posy > coord[1]:
				direction = "down"
			#print "player poss:{}, moving to:{} with direction:{}".format((player.posx, player.posy), coord, direction )
			if direction != None:
				threading.Thread(target=player.walk, args=(direction,)).start()
				threading.Thread(target=screen.move, args=(direction,)).start()

