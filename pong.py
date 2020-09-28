import pygame
import sys
import random
from enum import Enum

# Pygame Setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Game Window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Colors
light_grey = (200, 200, 200)
bg_color = pygame.Color('grey12')

# Ball Image
ball_image = pygame.image.load("images/corona.png")
ball_image = pygame.transform.scale(ball_image, (125,75))
ball = ball_image.get_rect(center=(screen_width / 2 -15, screen_height / 2 - 15))

# Opponent Paddle
paddle_image = pygame.image.load("images/mask.png")
paddle_image = pygame.transform.scale(paddle_image, (150,150))
left_image = pygame.transform.flip(paddle_image, True, False)
opponent = left_image.get_rect(center=(50, screen_height / 2 - 70)) # creates rectangle, same size as image

# Player Paddle
player = paddle_image.get_rect(center=(screen_width - 50, screen_height / 2 - 70)) # creates rectangle, same size as image

# Game Variables
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

# Score Text
player_score = 0
opponent_score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)

# Sound Effects
pong_sound = pygame.mixer.Sound("./media/pong.ogg")
score_sound = pygame.mixer.Sound("./media/score.ogg")

# Background Pictures
party = pygame.image.load("images/party.jpg").convert()
party = pygame.transform.scale(party, (screen_width,screen_height))

emergency = pygame.image.load("images/emergency.jpg").convert()
emergency = pygame.transform.scale(emergency, (screen_width,screen_height))

hospital = pygame.image.load("images/hospital.jpg").convert()
hospital = pygame.transform.scale(hospital, (screen_width,screen_height))

flatline = pygame.image.load("images/flatline.png").convert()
flatline = pygame.transform.scale(flatline, (screen_width,screen_height))

def display_background():
	global player_score, opponent_score

    # so function doesn't account for lower score when it hits a milestone
	if player_score > opponent_score:
		greater_score = player_score
	else:
		greater_score = opponent_score

    # milestone at scores 0, 5, 10, 15
	if greater_score == 15:
		screen.blit(flatline, [0,0])		
	if 10 <= greater_score < 15:
		screen.blit(hospital, [0,0])
	if 5 <= greater_score < 10:
		screen.blit(emergency, [0,0])
	if greater_score < 5:
		screen.blit(party, [0,0])

def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball Collision (Top or Bottom)
    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1

    # Player Scores
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        ball_restart()

    # Opponent Scores
    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        ball_restart()

    # Ball Collision (Player or Opponent)
    if ball.colliderect(player) or ball.colliderect(opponent):
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_x *= -1


def player_animation():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_ai():
    if opponent.top < ball.y:
        opponent.y += opponent_speed
    if opponent.bottom > ball.y:
        opponent.y -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_restart():
    global ball_speed_x, ball_speed_y

    # move ball to the center
    ball.center = (screen_width/2, screen_height/2)

    # start the ball in a random direction
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))


class State(Enum):
    menu = 1
    play = 2
    end = 3
    pause = 4


if __name__ == "__main__":
	# This sets the starting state to the main menu
    state = State.menu
    while True:
        
        # this is our state machine, we have one for the states in class State(Enum)
        if state is State.menu:
            # Creating the surface for text
            test_text = basic_font.render(
                f'Press any key to start playing - will change later', False, light_grey)

            screen.blit(test_text, (660, 470))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Check for any user input
                if event.type == pygame.KEYDOWN:
                    state = State.play
        elif state is State.play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player_speed -= 6
                    if event.key == pygame.K_DOWN:
                        player_speed += 6
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        player_speed += 6
                    if event.key == pygame.K_DOWN:
                        player_speed -= 6

            ball_animation()
            player_animation()
            opponent_ai()

            # Visuals
            screen.fill(bg_color)
            display_background()
            screen.blit(paddle_image, player)
            screen.blit(left_image, opponent)
            screen.blit(ball_image, ball)
            pygame.draw.aaline(screen, light_grey, (screen_width / 2,
                                                    0), (screen_width / 2, screen_height))

            # Creating the surface for text
            player_text = basic_font.render(
                f'{player_score}', False, light_grey)
            screen.blit(player_text, (660, 470))

            opponent_text = basic_font.render(
                f'{opponent_score}', False, light_grey)
            screen.blit(opponent_text, (600, 470))

        # Loop Timer
        pygame.display.flip()
        clock.tick(60)
