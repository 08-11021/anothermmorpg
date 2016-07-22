import pygame, sys
import time
import threading
from pygame.locals import *
from random import randint
from player import *
from screen import *
from tile import *

#Tamano de ventana
WIDTH = 608
HEIGHT = 416
#Tamano de sqm
SQM_SIZE=32


map = []
routeMap = []

#Metodo para dibujar elementos en el screen
def dibujar(ventana, player, screen):
	for i in xrange(0, 15):
		posI = i * SQM_SIZE
		for j in range(0, 21):
			posJ = j * SQM_SIZE
			ventana.blit(screen.pos[i, j].background,
						 (posJ - SQM_SIZE + screen.displacementX, posI - SQM_SIZE + screen.displacementY))
	ventana.blit(player.ImagePlayer, (posX, posY))
	pygame.display.update()

pygame.init()
ventana = pygame.display.set_mode((WIDTH, HEIGHT))
screen = screen()
pygame.display.set_caption("ZombieLand")
player = player()
ruta = []
# miFuente = pygame.font.Font("mifuente.otf")
# miTexto = miFuente.render("prueba fuente",0,(200,60,80))
# ventana.blit(miFuente, (posX,posY))
posY, posX = (HEIGHT / 2) - (SQM_SIZE/2), (WIDTH / 2) - (SQM_SIZE/2)

#Banderas para indicar que una tacla esta presionada:
flagLeft = False
flagRight = False
flagUp = False
flagDown = False

while True:
	#Crear un hilo para q dibuje la ventana
	threading.Thread(target=dibujar, args=(ventana, player, screen,)).start()

	#Lector de eventos
	for evento in pygame.event.get():

		#Evento de cerrar ventana
		if evento.type == QUIT:
			pygame.quit()
			sys.exit()

		#Evento de presion de tecla
		elif evento.type == pygame.KEYDOWN:

			#Tecla flecha izquierda
			if evento.key == K_LEFT:
				ruta = []
				flagLeft = True

			#Tecla flecha derecha
			elif evento.key == K_RIGHT:
				ruta = []
				flagRight = True

			#Tecla flecha arriba
			elif evento.key == K_UP:
				ruta = []
				flagUp = True

			#Tecla flecha abajo
			elif evento.key == K_DOWN:
				ruta = []
				flagDown = True

			#Tecla c (cambio de outfit provisional solo para probar los distintos sprites)
			elif evento.key == K_c:
				threading.Thread(target=player.nextOutfit).start()

		#Evento liberar tecla
		elif evento.type == pygame.KEYUP:
			if evento.key == K_LEFT:
				flagLeft = False
			elif evento.key == K_RIGHT:
				flagRight = False
			elif evento.key == K_UP:
				flagUp = False
			elif evento.key == K_DOWN:
				flagDown = False

		#Evento click del raton
		elif evento.type == pygame.MOUSEBUTTONDOWN:
			#Evento click izquierdo
			if pygame.mouse.get_pressed()[0] == 1:
				ruta = screen.getRoute(pygame.mouse.get_pos()[0] / SQM_SIZE, pygame.mouse.get_pos()[1] / SQM_SIZE, player.posx,
									   player.posy)

#Movimiento segun la bandera activada
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

##Movimiento si hay elementos en la ruta
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

