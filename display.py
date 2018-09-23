import pygame
from pygame.locals import *

RED = (255,0,0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 175, 0)
WHITE = (255, 255, 255)
GRAY = (175, 175, 175)
DARK_GRAY = (128, 128, 128)

TEXTURE_DIFFERENCE = 1
OBSTACLES_DIFFERENCE = 5

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
		if (self.position >= height):
			return 1
		return 0

class Display():
	def __init__(self):
		pygame.init()

		self.width = 600
		self.height = 400

		self.player_height = 375
		self.LEFT_BOUND_LIMIT = 75
		self.RIGHT_BOUND_LIMIT = 225
		
		# Variables for dealing with changing textures
		self.textures = []
		self.texture_count = 0 # count frames to update releasing another texture

		# Variables for dealing with hills
		self.road_pos = 300
		self.road_height = self.height - self.road_pos
		self.road_curve = -1
		self.pov = self.road_pos - 25

		# Variables for dealing with curves
		self.center_line = [0] * (self.road_height)
		self.offset = 0
		self.dxoffset = 0
		self.dxxoffset = 0
		self.straighten = 0 # Equals 1 when road curve is straightening out again

		# Variables for dealing with obstacles
		self.obstacles = []
		self.obstacles_count = 0

		self.background = pygame.image.load('assets/mountains.png')
		self.rect = self.background.get_rect()
		self.rect.left, self.rect.top = (-100, 0)		
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

	def update_hills(self):
		if (self.road_pos < 250):
			self.road_curve = 1
		if (self.road_pos > 350):
			self.road_curve = -1
		self.road_pos += self.road_curve
		if (self.road_curve >= 1): 
			self.road_curve += 1
		else:
			self.road_curve -= 1

	def left_curve(self):
		self.dxxoffset = -1

	def right_curve(self):
		self.dxxoffset = 1

	def update_centre(self):
		self.offset += self.dxoffset
		self.dxoffset += self.dxxoffset

		if (self.straighten == 1):
			self.center_line.pop(0)
			self.center_line.append(0)
			self.rect.left += 3 # Move background to add illusion of turning curve
		else:
			self.center_line.insert(0, self.offset)
			self.center_line.pop()

		if ((abs(self.offset) >= int(self.width/2) - 50) and (abs(self.dxxoffset) != 2)):
			self.offset = 0
			self.dxoffset = 0
			self.dxxoffset = 0
			self.straighten = 1
		if (self.center_line[0] == 0):
			self.straighten = 0
		print(self.center_line[0])

	def draw_road(self, height, pos, colours):
		for i in range(height):
			midpoint = int(self.width/2) # Midpoint of screen
			offset_index = (pos+i) - self.road_pos
			if (offset_index >= 100):
				offset_index = 99
			midline = self.center_line[offset_index] + midpoint # Middle line that determines curve
			obj_distance = pos + i - self.pov
			screen_distance = self.height - self.pov
			obj_lat = int((midpoint*obj_distance)/screen_distance)
			inner_boundary_1 = midline - obj_lat
			inner_boundary_2 = midline + obj_lat

			obj_lat_2 = int(((midpoint+15)*obj_distance)/screen_distance)
			outer_boundary_1 = midline - obj_lat_2
			outer_boundary_2 = midline + obj_lat_2

			pygame.draw.rect(self.screen, colours[0], (0, pos + (i), outer_boundary_1, 1)) # Grass
			
			boundary_width = inner_boundary_1 - outer_boundary_1
			pygame.draw.rect(self.screen, colours[1], (outer_boundary_1, pos + (i), boundary_width, 1)) # Boundary

			road_line_width = int((inner_boundary_2 - inner_boundary_1)/50)
			lane_width = int(((inner_boundary_2 - inner_boundary_1) - (road_line_width*2))/3)

			pygame.draw.rect(self.screen, colours[2], (inner_boundary_1, pos + (i), lane_width, 1)) # Road Lane 1
			pygame.draw.rect(self.screen, colours[3], (inner_boundary_1 + lane_width, pos + (i), road_line_width, 1)) # White Line
			lane_2_x = inner_boundary_1 + lane_width + road_line_width
			pygame.draw.rect(self.screen, colours[2], (lane_2_x, pos + (i), lane_width, 1)) # Road Lane 2
			pygame.draw.rect(self.screen, colours[3], (lane_2_x + lane_width, pos + (i), road_line_width, 1)) # White Line
			lane_3_x = inner_boundary_2 - lane_width
			pygame.draw.rect(self.screen, colours[2], (lane_3_x, pos + (i), lane_width, 1)) # Road Lane 3
			pygame.draw.rect(self.screen, colours[1], (inner_boundary_2, pos + (i), boundary_width, 1)) # Boundary
			pygame.draw.rect(self.screen, colours[0], (outer_boundary_2, pos + (i), self.width - outer_boundary_2, 1)) # Grass

	def update_display(self):
		self.update_centre()
		self.screen.blit(self.background, self.rect)
		self.draw_road((self.road_height), self.road_pos, (GREEN, RED, GRAY, WHITE))

		# Update count for each frame, every 2 frames add a new texture to Queue
		self.texture_count += 1
		if (self.texture_count > TEXTURE_DIFFERENCE):
			texture = Texture()
			self.textures.insert(0, texture)
			self.texture_count = 0

		#self.obstacles_count += 1
		if (self.obstacles_count > OBSTACLES_DIFFERENCE):
			obstacle = Texture()
			self.obstacles.insert(0, obstacle)
			self.obstacles_count = 0

		# Draw and update all textures i.e dark green lines that simulate 3D
		for t in self.textures:
			self.draw_road(t.height, (self.road_pos + t.position), (DARK_GREEN, WHITE, DARK_GRAY, DARK_GRAY))
			#pygame.draw.rect(self.screen, DARK_GREEN, (0, self.road_pos + t.position, self.width, t.height))
			if (t.update_texture(self.height)):
				self.textures.pop()
		
		for o in self.obstacles:
			pygame.draw.rect(self.screen, RED, (150, 100 + o.position, o.height, o.height))
			if (o.update_texture(self.height)):
				self.obstacles.pop()

		pygame.draw.circle(self.screen, RED, (self.pos[0]*2, self.player_height), 10, 0)

		pygame.display.flip()

	def is_done(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return 1
		return 0

	def __del__(self):
	    pygame.quit() 

