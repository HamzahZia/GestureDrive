import pygame
from pygame.locals import *

RED = (255,0,0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 175, 0)
TEXTURE_DIFFERENCE = 1

class Texture():
	def __init__(self):
		self.position = 0
		self.velocity = 0
		self.acceleration = 1
		self.height = 1

	def update_texture(self, height):
		self.velocity += self.acceleration
		self.position += self.velocity
		self.height += 1
		if (self.position > height):
			return 1
		return 0

class Display():
	def __init__(self):
		pygame.init()

		self.width = 600
		self.height = 400

		self.player_height = 250
		self.LEFT_BOUND_LIMIT = 75
		self.RIGHT_BOUND_LIMIT = 225
		self.textures = []
		self.texture_count = 0 # count frames to update releasing another texture

		self.background = pygame.image.load('assets/mountains.png')
		self.rect = self.background.get_rect()
		self.rect.left, self.rect.top = (0, 0)		
		self.pos = (150, self.player_height) # initial position of player
		self.screen=pygame.display.set_mode((self.width, self.height))

		pygame.display.set_caption('Display')
		#clock = pygame.time.Clock()
		self.screen.fill([255, 255, 255])

	def update_pos(self, pos):
		x = pos[0]
		y = pos[1]

		if (x < self.LEFT_BOUND_LIMIT):
			x = self.LEFT_BOUND_LIMIT

		if(self.RIGHT_BOUND_LIMIT < x):
			x = self.RIGHT_BOUND_LIMIT

		self.pos = (x, y)

	def update_display(self):
		self.screen.blit(self.background, self.rect)
		#for i in range(100):
		#	colour = GREEN
		#	if (i >= self.texture_position and i < self.texture_position + self.texture_height):
		#		colour = DARK_GREEN
		#	pygame.draw.rect(self.screen, colour, (0, 300 + (i), 600, 1))
		pygame.draw.rect(self.screen, GREEN, (0, 300, 600, 100))
		
		# Update count for each frame, every 20 frames add a new texture to Queue
		self.texture_count += 1
		if (self.texture_count > TEXTURE_DIFFERENCE):
			texture = Texture()
			self.textures.insert(0, texture)
			self.texture_count = 0

		# Draw and update all textures i.e dark green lines that simulate 3D
		for t in self.textures:
			pygame.draw.rect(self.screen, DARK_GREEN, (0, 300 + t.position, 600, t.height))
			if (t.update_texture(self.height)):
				self.textures.pop()
		
		pygame.draw.circle(self.screen, RED, (self.pos[0]*2, self.player_height), 10, 0)
		pygame.display.flip()


	def is_done(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return 1
		return 0

	def __del__(self):
	    pygame.quit() 

