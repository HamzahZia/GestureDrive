import pygame
from pygame.locals import *

red = (255,0,0)

class Display():
	def __init__(self):
		pygame.init()

		self.width = 640
		self.height = 480
		self.screen=pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption('Tether')

#		clock = pygame.time.Clock()

	def update_display(pos):
	    self.screen.fill(0)
	    #pos = pygame.mouse.get_pos()
	    pygame.draw.circle(screen, red, pos, 10, 0)

	    pygame.display.flip()

	def __del__(self):
	    pygame.quit() 
	    exit(0) 

