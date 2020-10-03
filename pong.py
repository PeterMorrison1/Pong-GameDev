import pygame
import sys
import os
import random
from enum import Enum

# Pygame Setup
pygame.mixer.pre_init(44100, -16, 2, 512)
os.environ['SDL_VIDEO_WINDOW_POS'] = "50,50"
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
ball_image = pygame.transform.scale(ball_image, (125,75)) # change numbers here to change size
ball = ball_image.get_rect(center=(screen_width / 2 -15, screen_height / 2 - 15))

# Opponent Paddle
paddle_image = pygame.image.load("images/mask.png")
paddle_image = pygame.transform.scale(paddle_image, (150,150)) # change numbers here to change size
left_image = pygame.transform.flip(paddle_image, True, False)
opponent = left_image.get_rect(center=(50, screen_height / 2 - 70)) # creates rectangle, same size as image

# Player Paddle
player = paddle_image.get_rect(center=(screen_width - 50, screen_height / 2 - 70)) # creates rectangle, same size as image
name = ""

# Game Variables
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

# Score Text
player_score = 0
opponent_score = 0

# Font Variables
basic_font = pygame.font.Font('freesansbold.ttf', 32)
big_font = pygame.font.Font('freesansbold.ttf', 50)

# Sound Effects
pong_sound = pygame.mixer.Sound("./media/coughing_cut2.ogg")
wall_sound = pygame.mixer.Sound("./media/Mario-jump-cut.ogg")
score_sound = pygame.mixer.Sound("./media/Pokemon_cut_2.ogg")
main_screen_sound = pygame.mixer.Sound("./media/Mario_Theme.ogg")

# Background Pictures
party = pygame.image.load("images/party.jpg")
party = pygame.transform.scale(party, (screen_width,screen_height))

emergency = pygame.image.load("images/emergency.jpg")
emergency = pygame.transform.scale(emergency, (screen_width,screen_height))

hospital = pygame.image.load("images/hospital.jpg")
hospital = pygame.transform.scale(hospital, (screen_width,screen_height))

flatline = pygame.image.load("images/flatline.jpg")
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
        pygame.mixer.stop()
        pygame.mixer.Sound.play(wall_sound)
        ball_speed_y *= -1

    # Player Scores
    if ball.left <= 0:
        pygame.mixer.stop()
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        ball_restart()

    # Opponent Scores
    if ball.right >= screen_width:
        pygame.mixer.stop()
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        ball_restart()

    # Ball Collision (Player or Opponent)
    if ball.colliderect(player) or ball.colliderect(opponent):
        pygame.mixer.stop()
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
    
def reset_game():
    global player_score, opponent_score, name
    player_score = 0
    opponent_score = 0
    name = ""

def end_screen():
    global winner, name

    #Score Display 
    opponent = basic_font.render(f'Opponent', False, light_grey)
    player = basic_font.render(f'Player', False, light_grey)
    opp_display_score = basic_font.render(f'{opponent_score}', False, light_grey)
    player_display_score = basic_font.render(f'{player_score}', False, light_grey)

    # Winning/Losing Line 
    opponent_line = big_font.render(f'Oh no, you have died!', False, light_grey)
    player_line = big_font.render(f'Congratulations, you have survived!', False, light_grey)

    play_again = basic_font.render("Click any button to play again", False, light_grey)

    # Display winning or losing line
    if winner == "player": 
        screen.blit(player_line, (200, 450))
    if winner == "opponent":
        screen.blit(opponent_line, (375,450))

    # Display Scores 
    screen.blit(opponent, (250, 100))
    screen.blit(player, (900, 100))
    screen.blit(opp_display_score, (320, 200))
    screen.blit(player_display_score, (940, 200))

    screen.blit(play_again, (400,700))


class State(Enum):
    menu = 1
    play = 2
    end = 3
    pause = 4


if __name__ == "__main__":
    # This sets the starting state to the main menu
    state = State.menu
    music_playing = False
    entering_name = False
    
    while True:
        # this is our state machine, we have one for the states in class State(Enum)
        if state is State.menu:
            screen.fill(bg_color)
            
            if music_playing is False:
                pygame.mixer.Sound.play(main_screen_sound)
                music_playing = True
        
            # Resets scores & name   
            player_score = 0
            opponent_score = 0
            
            # Creating the surface for text
            title_text = basic_font.render(f'COVID-19 Pong', False, light_grey)
            start_text = basic_font.render(f'Press any key to start playing', False, light_grey)

            screen.blit(title_text, (300, 100))
            screen.blit(start_text, (300, 270))

            # Updates the name input every frame
            if entering_name is True:
                name_text = basic_font.render(f'Name: {name}', False, light_grey)
                prompt_text = basic_font.render(f'Type your name, press enter when done', False, light_grey)
                screen.blit(prompt_text, (300, 425))
                screen.blit(name_text, (300, 475))
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Check for any user input
                if event.type == pygame.KEYDOWN:
                    entering_name = True
                    if event.key == pygame.K_RETURN:
                        entering_name = False
                        state = State.play
                    else:
                        name = name + str(event.unicode)
        
        elif state is State.end:
            screen.fill(bg_color)
            name = ""
            #End screen function 
            end_screen()         

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN: # To start new game
                    print(event)
                    if event.key == pygame.K_RETURN:
                        state = State.menu
        
        elif state is State.pause:
            screen.fill(bg_color)

            pause_text = basic_font.render(f'Press Enter to Resume', False, light_grey)
            screen.blit(pause_text, (300, 475))
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN: # To start new game
                    if event.key == pygame.K_RETURN:
                        state = State.play

        elif state is State.play:
            music_playing = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player_speed -= 6
                    if event.key == pygame.K_DOWN:
                        player_speed += 6
                    if event.key == pygame.K_RETURN:
                        state = State.pause
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        player_speed += 6
                    if event.key == pygame.K_DOWN:
                        player_speed -= 6
            
            ball_animation()
            player_animation()
            opponent_ai()

            # End Score
            if player_score == 15: 
                state = State.end
                winner = "player"
                print("end")
            if opponent_score == 15:
                state = State.end
                winner = "opponent"
                print("end")

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
