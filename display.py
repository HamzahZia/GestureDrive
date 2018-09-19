import pygame
from pygame.locals import *

red = (255,0,0)

class Display():
	def __init__(self):
		pygame.init()

		self.width = 300
		self.height = 200
		self.screen=pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption('Display')
		#clock = pygame.time.Clock()

	def update_display(self, pos):
	    self.screen.fill(0)
	    #pos = pygame.mouse.get_pos()
	    pygame.draw.circle(self.screen, red, (pos[0], 100), 10, 0)
	    pygame.display.flip()

	def leave(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return 1
		return 0

	def __del__(self):
	    pygame.quit() 

