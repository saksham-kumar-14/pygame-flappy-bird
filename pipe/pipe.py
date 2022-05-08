import pygame, random


class Pipe:
	def __init__(self, up, pipe_width, pipe_height, x, y):
		self.pipe_width, self.pipe_height = pipe_width, pipe_height
		self.up = up
		self.pipe = pygame.transform.scale(pygame.image.load("images/pipe-images/pipe.png"), (pipe_width, pipe_height))
		if up:
			self.pipe = pygame.transform.rotate(self.pipe, 180)

		self.x = x
		self.y = y

	def draw(self, screen):
		screen.blit(self.pipe, (self.x, self.y))

	def update(self, new_x):
		self.x = new_x

	def get_coordinates(self):
		return [self.x, self.y]

	def generate_random_height(self, screen_height):
		pipe_height = random.randrange(100,250)
		self.pipe = pygame.transform.scale(self.pipe, (self.pipe_width,pipe_height))
		if self.up:
			self.y = screen_height - pipe_height
