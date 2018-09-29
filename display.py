import pygame
from pygame.locals import *
import spritesheet
from texture import Texture
import random

RED = (255,0,0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 175, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
DARK_GRAY = (128, 128, 128)

TEXTURE_DIFFERENCE = 1
TREE_MULTIPLIER = 10
ROCK_MULTIPLIER = 5
CAR_MULTIPLIER = 4
SPEEDSIGN_MULTIPLIER = 10

ROAD_PROP_DELAY = 2000
ROAD_OBSTACLE_DELAY = 3000
ROAD_CURVE_DELAY = 18000

random.seed()

class Display():
	def __init__(self):
		pygame.init()

		self.width = 600
		self.height = 400

		self.player_height = 315
		self.LEFT_BOUND_LIMIT = 75
		self.RIGHT_BOUND_LIMIT = 225
		
		# Variables for dealing with changing textures
		self.textures = []
		self.texture_count = 0 # count frames to update releasing another texture

		# Variables for dealing with hills
		self.road_pos = 250
		self.road_height = self.height - self.road_pos
		self.road_curve = -1
		self.pov = self.road_pos - 25

		# Variables for dealing with curves
		self.center_line = [0] * (self.road_height)
		self.offset = 0
		self.dxoffset = 0
		self.dxxoffset = 0
		self.straighten = 0 # Equals 1 when road curve is straightening out again
		self.curve_switch = 1 # Every n seconds alternate between emitting a left curve and right 
		self.straight_count = 0 # Variable to hold curve state before straightening out

		# Variables for dealing with props
		self.props = []
		# Variables for dealing with obstacles
		self.obstacles = []

		self.background = pygame.image.load('assets/mountains.png')
		self.rect = self.background.get_rect()
		self.rect.left, self.rect.top = (-40, 0)		
		self.pos = (150, self.player_height) # initial position of player
		self.screen=pygame.display.set_mode((self.width, self.height))

		self.road_prop_event = pygame.USEREVENT + 1
		self.road_curve_event = pygame.USEREVENT + 2
		self.road_obstacle_event = pygame.USEREVENT + 3

		pygame.display.set_caption('Display')
		clock = pygame.time.Clock()
		pygame.time.set_timer(self.road_prop_event, ROAD_PROP_DELAY)
		pygame.time.set_timer(self.road_curve_event, ROAD_CURVE_DELAY)
		pygame.time.set_timer(self.road_obstacle_event, ROAD_OBSTACLE_DELAY)
		self.screen.fill([255, 255, 255])

		# Load in player sprites from sprite sheet
		player_ss = spritesheet.spritesheet('assets/redcar.png')
		self.player_images = player_ss.images_at(((0, 0, 100, 70), (100, 0, 100, 70), (200, 0, 95, 70)), colorkey=(186, 254, 180))
		self.player = self.player_images[0] # initialize to default straight car
		self.tree_ss = spritesheet.spritesheet('assets/tree.png')
		self.tree = self.tree_ss.image_at((0, 0, 1814, 2400), colorkey=(0, 0, 0))
		self.rock_ss = spritesheet.spritesheet('assets/rock.png')
		self.rock = self.rock_ss.image_at((0, 0, 720, 500), colorkey=(0, 0, 0))
		self.speedsign_ss = spritesheet.spritesheet('assets/speedsign.jpg')
		self.speedsign = self.speedsign_ss.image_at((0, 0, 141, 200), colorkey=(0, 255, 0))
		self.bluecar_ss = spritesheet.spritesheet('assets/bluecar.png')
		self.bluecar = self.bluecar_ss.image_at((0, 0, 100, 67), colorkey=(186, 254, 180))

	def update_pos(self, pos):
		x = pos[0]
		y = pos[1]

		if (x < self.LEFT_BOUND_LIMIT):
			x = self.LEFT_BOUND_LIMIT
		elif(self.RIGHT_BOUND_LIMIT < x):
			x = self.RIGHT_BOUND_LIMIT


		if (x < self.pos[0] - 3):
			self.player = self.player_images[2]
		elif (x > self.pos[0] + 3):
			self.player = self.player_images[1]

		if (x < self.pos[0] - 10):
			self.pos = (self.pos[0] - 10, y)
		elif (x > self.pos[0] + 6):
			self.pos = (self.pos[0] + 10, y)
		else: 
			self.pos = (x, y)

	def update_textures(self):
		# Draw and update all textures i.e dark green lines that simulate 3D
		for t in self.textures:
			self.draw_road(t.height, (self.road_pos + t.position), (DARK_GREEN, WHITE, DARK_GRAY, DARK_GRAY))
			#pygame.draw.rect(self.screen, DARK_GREEN, (0, self.road_pos + t.position, self.width, t.height))
			if (t.update_texture(self.height)):
				self.textures.pop()

	def update_props(self):
		for o in self.props:
			(ib_1, ib_2, ob_1, ob_2) = self.line_calculation(self.road_pos + o.position)
			if (o.offset > 0):
				o_x = ob_2 + 30
			elif (o.offset < 0):
				o_x = ob_1 - 100
			
			if (o.type == "tree"):
				o_width = int((o.height/4) * 3) * TREE_MULTIPLIER
				o_height = o.height * TREE_MULTIPLIER
				prop = pygame.transform.scale(self.tree, (o_width, o_height))				
				prop_rect = pygame.Rect((o_x, self.road_pos + o.position - o_height, o_width, o_height))
			elif (o.type == "rock"):
				o_width = int((o.height/25) * 36) * ROCK_MULTIPLIER
				o_height = o.height * ROCK_MULTIPLIER
				prop = pygame.transform.scale(self.rock, (o_width, o_height))				
				prop_rect = pygame.Rect((o_x, self.road_pos + o.position - o_height, o_width, o_height))
			elif (o.type == "speedsign"):
				o_width = int((o.height/10) * 7) * SPEEDSIGN_MULTIPLIER
				o_height = o.height * SPEEDSIGN_MULTIPLIER
				prop = pygame.transform.scale(self.speedsign, (o_width, o_height))				
				prop_rect = pygame.Rect((o_x, self.road_pos + o.position - o_height, o_width, o_height))
			
			self.screen.blit(prop, prop_rect)
			if (o.update_texture(self.height)):
				self.props.pop()

	def update_obstacles(self):
			for o in self.obstacles:
				o_width = int((o.height/67) * 100) * CAR_MULTIPLIER
				o_height = o.height * CAR_MULTIPLIER
				bluecar = pygame.transform.scale(self.bluecar, (o_width, o_height))
				(ib_1, ib_2, ob_1, ob_2) = self.line_calculation(self.road_pos + o.position)
				offset = int((3*(ib_2 - ib_1)/6) - o_width/2)
				o_x = ib_1 + offset
				
				obst_rect = pygame.Rect((o_x, self.road_pos + o.position - o_height, o_width, o_height))
				self.screen.blit(bluecar, obst_rect)
				if (o.update_texture(self.height)):
					self.obstacles.pop()

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
		self.dxoffset += self.dxxoffset
		self.offset += int(self.dxoffset/4)

		if (self.straighten == 1):
			if (self.straight_count == 10 or self.straight_count == 0):
				self.straight_count == 0
				for n in range(2):
					self.center_line.pop(0) # Action repeated twice to exagerate curve
					self.center_line.append(0)
			elif (self.straight_count > 0):
				self.straight_count += 1

			if (self.center_line[10] != 0):
				if (self.offset < 0):
					self.rect.left += 2 # Move background to add illusion of turning curve
				else:
					self.rect.left -= 2
		else:
			for n in range(2):
				self.center_line.insert(0, self.offset)
				self.center_line.pop()

		if (abs(self.offset) >= int(self.width/2) - 200 and self.straighten == 0):		
			if (self.offset < 0):
				self.rect.left += 1 # Move background to add illusion of turning curve
			else:
				self.rect.left -= 1

		if (abs(self.offset) >= int(self.width/2) - 150 and self.straighten == 0):
			self.straighten = 1
			self.straight_count = 1
		elif (self.center_line[0] == 0 and self.straighten == 1):
			self.straighten = 0
			self.offset = 0
			self.dxoffset = 0
			self.dxxoffset = 0

	def line_calculation(self, loc):
		midpoint = int(self.width/2) # Midpoint of screen
		offset_index = loc - self.road_pos
		if (offset_index >= self.road_height):
			offset_index = self.road_height - 1
		midline = self.center_line[offset_index] + midpoint # Middle line that determines curve
		obj_distance = loc - self.pov
		screen_distance = self.height - self.pov
		obj_lat = int((midpoint*obj_distance)/screen_distance)
		inner_boundary_1 = midline - obj_lat
		inner_boundary_2 = midline + obj_lat

		obj_lat_2 = int(((midpoint+15)*obj_distance)/screen_distance)
		outer_boundary_1 = midline - obj_lat_2
		outer_boundary_2 = midline + obj_lat_2

		return (inner_boundary_1, inner_boundary_2, outer_boundary_1, outer_boundary_2)

	def draw_road(self, height, pos, colours):
		for i in range(height):
			(inner_boundary_1, inner_boundary_2, outer_boundary_1, outer_boundary_2) = self.line_calculation(pos+i)

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
		if (self.dxxoffset != 0):
			self.update_centre()
		self.screen.blit(self.background, self.rect)
		self.draw_road((self.road_height), self.road_pos, (GREEN, RED, GRAY, WHITE))

		# Update count for each frame, every 2 frames add a new texture to Queue
		self.texture_count += 1
		if (self.texture_count > TEXTURE_DIFFERENCE):
			texture = Texture()
			self.textures.insert(0, texture)
			self.texture_count = 0

		self.update_textures()
		self.update_props()
		self.update_obstacles()

		player_rect = pygame.Rect((self.pos[0] - 25)*2, self.player_height, 100, 70)
		#self.screen.blit(self.bluecar, (50, self.player_height, 100, 67))
		self.screen.blit(self.player, player_rect)
		self.player = self.player_images[0] # reset car to straight position
		pygame.display.flip()

	def is_done(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return 1
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.left_curve()
				if event.key == pygame.K_RIGHT:
					self.right_curve()
			if event.type == self.road_prop_event:
				choice = random.randint(1,5)
				if choice < 4:
					prop = Texture() # left tree
					prop.set_type("tree")
					prop.set_offset(-1)
					prop.set_boost(4)
					self.props.insert(0, prop)
					prop2 = Texture() # right tree
					prop2.set_type("tree")
					prop2.set_boost(4)
					prop2.set_offset(1)
					self.props.insert(0, prop2)
				else:
					prop = Texture() # rock
					prop.set_type("speedsign")
					if (choice == 4):
						prop.set_offset(-1)
					elif (choice == 5):
						prop.set_offset(1)
					prop.set_boost(4)
					self.props.insert(0, prop)

			if event.type == self.road_curve_event:
				if (self.curve_switch == 0):
					self.left_curve()
					self.curve_switch = 1
				elif (self.curve_switch == 1):
					self.right_curve()
					self.curve_switch = 0
			if event.type == self.road_obstacle_event:
				obstacle = Texture() # left tree
				self.obstacles.insert(0, obstacle)
		return 0

	def __del__(self):
	    pygame.quit() 

