import pygame
import numpy as np
import argparse
import levels

# Initialize Pygame
pygame.init()
pygame.mouse.set_visible(False)

# Set up some constants
WIDTH, HEIGHT = 800, 600
MAP_WIDTH, MAP_HEIGHT = 20, 20

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the player
player_x, player_y = 1, 1
player_angle = 0

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--level", default="level1", help="Level to load")
args = parser.parse_args()

# Load the specified level
map_data = levels.levels[args.level]

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            # Get mouse movement
            dx, dy = pygame.mouse.get_rel()
            
            # Update player angle based on mouse movement
            player_angle += dx * 0.01  # Adjust sensitivity as needed

            # Keep mouse centered
            pygame.mouse.set_pos(WIDTH // 2, HEIGHT // 2)

    # Cast rays
    rays = []
    for i in range(WIDTH):
        ray_angle = player_angle + (i - WIDTH / 2) / WIDTH * 0.5
        ray_x, ray_y = player_x, player_y
        while True:
            ray_x += np.cos(ray_angle)
            ray_y += np.sin(ray_angle)
            if int(ray_y) >= 0 and int(ray_y) < MAP_HEIGHT and int(ray_x) >= 0 and int(ray_x) < MAP_WIDTH:
                if map_data[int(ray_y)][int(ray_x)] == '1':
                    break
            else:
                break
        rays.append((ray_x, ray_y))

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_x += np.cos(player_angle) * 0.1
        player_y += np.sin(player_angle) * 0.1
    if keys[pygame.K_s]:
        player_x -= np.cos(player_angle) * 0.1
        player_y -= np.sin(player_angle) * 0.1
    if keys[pygame.K_a]:
        player_angle -= 0.1
    if keys[pygame.K_d]:
        player_angle += 0.1

    # Draw everything
    screen.fill((192, 192, 192))  # Fill the background gray for the floor
    for i, ray in enumerate(rays):
        # Calculate distance to the wall
        distance = np.sqrt((ray[0] - player_x) ** 2 + (ray[1] - player_y) ** 2) + 0.001

        # Calculate wall height based on distance
        wall_height = HEIGHT / (distance / 20)

        # Calculate wall position on screen
        wall_x = i * 2
        wall_y = HEIGHT / 2 - wall_height / 2

        # Draw the wall slice
        color = 255 - distance * 2  # Make walls darker with distance
        pygame.draw.rect(screen, (color, color, color), (wall_x, wall_y, 1, wall_height))

    # Draw the player
    pygame.draw.circle(screen, (255, 0, 0), (int(player_x * 20), int(player_y * 20)), 5)

    pygame.display.flip()

pygame.quit()
