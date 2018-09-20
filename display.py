import pygame
from pygame.locals import *

red = (255,0,0)

class Display():
	def __init__(self):
		pygame.init()

		self.width = 600
		self.height = 400

		self.player_height = 350
		self.LEFT_BOUND_LIMIT = 75
		self.RIGHT_BOUND_LIMIT = 225

		self.pos = (150, self.player_height) # initial position of player
		self.screen=pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption('Display')
		#clock = pygame.time.Clock()

	def update_pos(self, pos):
		x = pos[0]
		y = pos[1]

		if (x < self.LEFT_BOUND_LIMIT):
			x = self.LEFT_BOUND_LIMIT

		if(self.RIGHT_BOUND_LIMIT < x):
			x = self.RIGHT_BOUND_LIMIT

		self.pos = (x, y)

	def update_display(self):
	    self.screen.fill(0)
	    pygame.draw.circle(self.screen, red, (self.pos[0]*2, self.player_height), 10, 0)
	    pygame.display.flip()

	def is_done(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return 1
		return 0

	def __del__(self):
	    pygame.quit() 

