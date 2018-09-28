class Texture():
	def __init__(self):
		self.position = 0
		self.velocity = 0
		self.acceleration = 4
		self.height = 1
		self.offset = 0

	def set_offset(self, offset):
		self.offset = offset

	def update_texture(self, height):
		self.velocity += self.acceleration
		self.position += self.acceleration * self.velocity
		self.height += self.acceleration * 1
		if (self.position >= height):
			return 1
		return 0