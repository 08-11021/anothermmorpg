import pygame, sys
import time
import threading
from pygame.locals import *
from random import randint
from player import *
from screen import *
from tile import *
from multiprocessing import Process, Lock

#Tamano de ventana
WIDTH = 608
HEIGHT = 416


SCREEN_WIDTH = WIDTH/32
SCREEN_HEIGHT = HEIGHT/32
#Tamano de sqm
SQM_SIZE=32


map = []
routeMap = []
mutex = Lock()
counter=0

#Metodo para dibujar elementos en el screen
def dibujar(ventana, player, screen, mutex):
	while (True):
		mutex.acquire()
		for j in xrange(0, SCREEN_HEIGHT+2):
			posJ = j * SQM_SIZE
			y= (SCREEN_HEIGHT/2+1)-j+player.posy
			for i in range(0, SCREEN_WIDTH+2):
				posI = i * SQM_SIZE
				x = i - (SCREEN_WIDTH / 2+1) + player.posx
				ventana.blit(screen.pos[x, y].background,
							 (posI - SQM_SIZE + screen.displacementX, posJ - SQM_SIZE + screen.displacementY))
		ventana.blit(player.ImagePlayer, (posX, posY))
		mutex.release()
		pygame.display.update()


pygame.init()
ventana = pygame.display.set_mode((WIDTH, HEIGHT))
player = player()
screen = screen(player.posx,player.posy)
pygame.display.set_caption("ZombieLand")

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
draw= threading.Thread(target=dibujar, args=(ventana, player, screen, mutex,)).start() #falta pasar los parametros por referencia
while True:
	#Crear un hilo para q dibuje la ventana


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
				ruta = screen.getRoute((pygame.mouse.get_pos()[0] / SQM_SIZE)-(SCREEN_WIDTH/2)+player.posx,
									   (SCREEN_HEIGHT / 2)-pygame.mouse.get_pos()[1] / SQM_SIZE+player.posy,
									   player.posx,
									   player.posy)

#Movimiento segun la bandera activada
	if flagLeft:
		if player.status == "waiting":
			threading.Thread(target=player.walk, args=("left",)).start()
			threading.Thread(target=screen.move, args=("left",mutex,player,)).start()#falta pasar los parametros por referencia
	elif flagRight:
		if player.status == "waiting":
			threading.Thread(target=player.walk, args=("right",)).start()
			threading.Thread(target=screen.move, args=("right",mutex,player,)).start()#falta pasar los parametros por referencia
	elif flagUp:
		if player.status == "waiting":
			threading.Thread(target=player.walk, args=("up",)).start()
			threading.Thread(target=screen.move, args=("up",mutex,player, )).start()#falta pasar los parametros por referencia
	elif flagDown:
		if player.status == "waiting":
			threading.Thread(target=player.walk, args=("down",)).start()
			threading.Thread(target=screen.move, args=("down",mutex,player, )).start()#falta pasar los parametros por referencia

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
				threading.Thread(target=screen.move, args=(mutex,direction,player,)).start()#falta pasar los parametros por referencia
