class Texture():
	def __init__(self):
		self.position = 0
		self.velocity = 0
		self.acceleration = 1	
		self.boost = 0
		self.height = 1
		self.offset = 0

	def set_offset(self, offset):
		self.offset = offset

	def set_boost(self, boost):
		self.boost = boost

	def set_type(self, type):
		self.type = type

	def update_texture(self, height):
		self.velocity += self.acceleration
		self.position += self.velocity + self.boost
		self.height += self.acceleration
		if (self.position >= height):
			return True
		return False