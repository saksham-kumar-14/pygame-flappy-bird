import pygame, sys, random, time

pygame.display.set_caption("Flappy Bird")
icon = pygame.transform.scale(pygame.image.load("./images/bird-images/bird1.png"), (30,30))
pygame.display.set_icon(icon)
pygame.init()
pygame.font.init()

from bird.bird import Bird
from pipe.pipe import Pipe

WIDTH, HEIGHT = 900,600
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 50

# sprites
BG_IMG = pygame.transform.scale(pygame.image.load("./images/background-images/bg.png"), (WIDTH, HEIGHT) )
GROUND_IMG = pygame.transform.scale(pygame.image.load("./images/background-images/ground.png"), (WIDTH,100))

# background sound
pygame.mixer.music.load("./sound-effects/bg.mp3")
pygame.mixer.music.play(-1)


def welcome_screen():
	global BG_IMG, GROUMD_IMG

	WELCOME_SCREEN_1 = pygame.transform.scale(pygame.image.load("./images/welcome-screen-images/welcome_screen_1.png"), (WIDTH//2,150))
	WELCOME_SCREEN_2 = pygame.transform.scale(pygame.image.load("./images/welcome-screen-images/welcome_screen_2.png"), (WIDTH//2,50))
	WELCOME_SCREEN_3 = pygame.transform.scale(pygame.image.load("./images/welcome-screen-images/welcome_screen_3.png"), (100,100))
	WELCOME_SCREEN_4 = pygame.transform.scale(pygame.image.load("./images/welcome-screen-images/welcome_screen_4.png"), (100,100))

	negative_rotation = False
	rotation_count = 0

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
				pygame.quit()
				sys.exit()

		SCREEN.fill(( 0,0,0 ))
		SCREEN.blit(BG_IMG, (0,0))
		SCREEN.blit(GROUND_IMG, (0,HEIGHT-GROUND_IMG.get_height()))
		SCREEN.blit(WELCOME_SCREEN_1, ((WIDTH- WELCOME_SCREEN_1.get_width())//2 ,0))
		SCREEN.blit(WELCOME_SCREEN_2, ( (WIDTH- WELCOME_SCREEN_2.get_width())//2 , ( (HEIGHT- WELCOME_SCREEN_2.get_height())//2 ) ))
		SCREEN.blit(WELCOME_SCREEN_3, (25, HEIGHT-300))
		SCREEN.blit(WELCOME_SCREEN_4, (WIDTH- WELCOME_SCREEN_4.get_width()-25, HEIGHT-300))

		if rotation_count == 25:
			if negative_rotation:
				rotation_angle = -90
			else:
				rotation_angle = 90

			WELCOME_SCREEN_3 = pygame.transform.rotate(WELCOME_SCREEN_3, rotation_angle)
			WELCOME_SCREEN_4 = pygame.transform.rotate(WELCOME_SCREEN_4, rotation_angle)

			negative_rotation = not negative_rotation
			rotation_count = 0
		
		rotation_count += 1

		if pygame.key.get_pressed()[pygame.K_SPACE]:
			break

		CLOCK.tick(FPS)
		pygame.display.update()

	
def main():
	global BG_IMG, GROUND_IMG

	# variables for the main game
	bird =  Bird(WIDTH, HEIGHT)
	gravity = 7
	bird_y_vel = 7
	bird_x_vel = 4
	bird_x_vel_counter = 0

	pipe_width = 60
	all_pipe_pairs = []
	current_pipe_x = 160
	total_pipes = 5
	pipe_bias = ((WIDTH-current_pipe_x) - ((total_pipes-1)*pipe_width)) // (total_pipes-1)


	for i in range(total_pipes):
		temp = []
		pipe_height = random.randrange(100,250)
		temp.append(Pipe(False, pipe_width, pipe_height, current_pipe_x,0))
		pipe_height = random.randrange(100,250)
		temp.append(Pipe(True, pipe_width, pipe_height, current_pipe_x, HEIGHT-pipe_height))
		all_pipe_pairs.append(temp)

		current_pipe_x += (pipe_bias + pipe_width)


	# score variables
	score = 0
	font = pygame.font.Font("freesansbold.ttf", 32)
	pipe_index_to_pass = 0

	game_over = False

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
				pygame.quit()
				sys.exit()


		# drawing stuff
		SCREEN.fill(( 0,0,0 ))
		SCREEN.blit(BG_IMG,(0,0))
		SCREEN.blit(GROUND_IMG, (0,HEIGHT-GROUND_IMG.get_height()))

		# drawing bird
		bird.draw(SCREEN)

		# moving the bird
		bird_x, bird_y = bird.get_coordinates()
		bird.update(bird_x, bird_y+gravity)
		if pygame.key.get_pressed()[pygame.K_UP]:
			bird.update(bird_x, bird_y-bird_y_vel)

		# drawing obstacles
		for i in all_pipe_pairs:
			for j in i:
				j.draw(SCREEN)

		# moving the background pipes
		for i in all_pipe_pairs:
			for j in i:
				j.update(j.get_coordinates()[0]- bird_x_vel)

		# checking the disappearing pipes 
		for i in all_pipe_pairs:
			for j in i:
				x = j.get_coordinates()[0]
				if x < 0:
					j.update(WIDTH)
					j.generate_random_height(HEIGHT)

		# increasing velocity
		bird_x_vel_counter += 1
		if bird_x_vel_counter == 250:
			bird_x_vel_counter = 0
			bird_x_vel += 1


		# collision detection
		for i in all_pipe_pairs:
			for j in i:
				if bird.collision_detected(j):
					game_over = True
					pygame.display.update()

		if bird_y < 0 or (bird_y > HEIGHT-bird.height):
			game_over = True
			pygame.display.update()

		if game_over:
			game_over_img = pygame.transform.scale(pygame.image.load("./images/background-images/game_over.png"), (200,50))
			SCREEN.blit(game_over_img, (WIDTH//2-(game_over_img.get_width()/2), HEIGHT//2-(game_over_img.get_height()/2) ))
			pygame.display.update()
			time.sleep(3)
			break

		# incrementing score
		if all_pipe_pairs[pipe_index_to_pass][0].x + bird_x_vel >= bird_x >= all_pipe_pairs[pipe_index_to_pass][0].x:
			score += 1
			if pipe_index_to_pass == len(all_pipe_pairs)-1:
				pipe_index_to_pass = 0
			else:
				pipe_index_to_pass += 1

		# displaying score
		score_font = font.render(f"Score: {str(score)}", True, (255,0,0))
		SCREEN.blit(score_font, (0,0))


		CLOCK.tick(FPS)
		pygame.display.update()


if __name__ == '__main__':

	while True:
		welcome_screen()
		main()