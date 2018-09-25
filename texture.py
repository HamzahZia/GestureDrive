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