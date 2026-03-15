import pygame
import random
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")

font = pygame.font.SysFont("Arial", 50)
small_font = pygame.font.SysFont("Arial", 30)

rock_btn = pygame.Rect(100, 420, 180, 80)
paper_btn = pygame.Rect(310, 420, 180, 80)
scissor_btn = pygame.Rect(520, 420, 180, 80)

player_choice = None
computer_choice = None
result = ""

player_score = 0
computer_score = 0


def check_winner(player, computer):

    if player == computer:
        return "Draw"

    if player == "rock" and computer == "scissor":
        return "You Win"

    if player == "paper" and computer == "rock":
        return "You Win"

    if player == "scissor" and computer == "paper":
        return "You Win"

    return "Computer Wins"


running = True

while running:

    screen.fill((30, 30, 30))

    title = font.render("Rock Paper Scissors", True, (255,255,255))
    screen.blit(title,(220,20))

    instruction = small_font.render("Click Rock, Paper or Scissors",True,(200,200,200))
    screen.blit(instruction,(250,100))

    score_text = small_font.render(f"You: {player_score}   Computer: {computer_score}",True,(255,255,255))
    screen.blit(score_text,(300,150))

    pygame.draw.rect(screen,(200,0,0),rock_btn)
    pygame.draw.rect(screen,(0,200,0),paper_btn)
    pygame.draw.rect(screen,(0,0,200),scissor_btn)

    rock_text = small_font.render("Rock",True,(255,255,255))
    paper_text = small_font.render("Paper",True,(255,255,255))
    scissor_text = small_font.render("Scissor",True,(255,255,255))

    screen.blit(rock_text,(150,445))
    screen.blit(paper_text,(370,445))
    screen.blit(scissor_text,(565,445))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse = pygame.mouse.get_pos()

            if rock_btn.collidepoint(mouse):
                player_choice = "rock"

            if paper_btn.collidepoint(mouse):
                player_choice = "paper"

            if scissor_btn.collidepoint(mouse):
                player_choice = "scissor"

            if player_choice:

                computer_choice = random.choice(["rock","paper","scissor"])

                result = check_winner(player_choice, computer_choice)

                if result == "You Win":
                    player_score += 1

                if result == "Computer Wins":
                    computer_score += 1


    if player_choice:

        player_text = small_font.render(f"You chose: {player_choice}",True,(255,255,255))
        comp_text = small_font.render(f"Computer chose: {computer_choice}",True,(255,255,255))
        result_text = font.render(result,True,(255,255,0))

        screen.blit(player_text,(300,220))
        screen.blit(comp_text,(300,260))
        screen.blit(result_text,(300,320))

        pygame.display.update()
        pygame.time.delay(1500)

        player_choice = None
        computer_choice = None
        result = ""

    pygame.display.update()