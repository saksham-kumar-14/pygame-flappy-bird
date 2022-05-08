import pygame

BIRD_WIDTH, BIRD_HEIGHT = 50,50

# sprites
DEFEATED_BIRD = pygame.transform.scale(pygame.image.load("images/bird-images/defeated_bird.png"), (BIRD_WIDTH, BIRD_HEIGHT))

ALL_BIRDS = []
for i in range(3):
	ALL_BIRDS.append(pygame.transform.scale(pygame.image.load(f"images/bird-images/bird{i+1}.png") ,(BIRD_WIDTH, BIRD_HEIGHT) ))

class Bird:
	def __init__(self, screen_width ,screen_height):
		self.screen_width, self.screen_height = screen_width, screen_height
		self.width = BIRD_WIDTH
		self.height = BIRD_HEIGHT
		self.all_birds = ALL_BIRDS
		self.current_bird = self.all_birds[0]
		self.current_bird_index = 0
		self.change_bird_count = 0

		self.x, self.y =  50, self.screen_height//2

	def draw(self, screen):
		screen.blit(self.current_bird, (self.x, self.y))

	def update(self, new_x, new_y):
		self.x = new_x
		self.y = new_y
		
		self.change_bird_count += 1
		if self.change_bird_count == 30:
			self.change_bird_count = 0
			if self.current_bird_index == len(self.all_birds)-1:
				self.current_bird_index = 0
			else:
				self.current_bird_index += 1
			self.current_bird = self.all_birds[self.current_bird_index]


	def collision_detected(self,obstacle):
		bird_rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
		obstacle_rectangle = pygame.Rect(obstacle.x, obstacle.y, obstacle.pipe_width, obstacle.pipe_height)

		if pygame.Rect.colliderect(bird_rectangle, obstacle_rectangle):
			return True

		return False

	def game_over(self):
		pass

	def get_coordinates(self):
		return [self.x, self.y]


