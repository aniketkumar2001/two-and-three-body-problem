
import numpy as np
import pygame
import sys

pygame.init()

SCREEN_WIDTH = 1550
SCREEN_HEIGHT = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

star_pos = np.array([772.50, 397.5])
pos = np.array([872.5, 400], dtype=np.float64)
vel = np.array([0, -100], dtype=np.float64)
thrust = 50
k = 1000000  # GM Star

dt = 1 / 60

trail_length = 100  # Number of previous positions to remember
trail_positions = []  # List to store previous positions

# Font for displaying text
font = pygame.font.Font(None, 28)

def add_gravitational_force(obj_pos, obj_vel):
    s = star_pos - obj_pos
    s_mod = np.linalg.norm(s)
    acc = (k * s) / (s_mod ** 3)
    obj_vel += acc * dt
    obj_pos += obj_vel * dt
    return obj_pos, obj_vel

def normalize_unit_vector(r):
    r = np.append(r, 0)
    r0 = np.array([0, 0, 1], dtype=np.float64)
    rf = np.cross(r0, r)
    rf = np.delete(rf, 2)
    mag_rf = np.linalg.norm(rf)
    unit_perp_r = rf / mag_rf
    return unit_perp_r

def handle_movement(key_state, velocity):
    unit_vel = velocity / np.linalg.norm(velocity)
    norm_unit_vel = normalize_unit_vector(velocity)

    radius_vector = pos - np.array(pygame.mouse.get_pos())
    unit_radius_vector = radius_vector / np.linalg.norm(radius_vector)

    if key_state[pygame.K_a]:
        velocity -= thrust * dt * norm_unit_vel
    if key_state[pygame.K_d]:
        velocity += thrust * dt * norm_unit_vel
    if key_state[pygame.K_w]:
        velocity += thrust * dt * unit_vel
    if key_state[pygame.K_s]:
        velocity -= thrust * dt * unit_vel
    if key_state[pygame.K_SPACE]:
        velocity += thrust * dt * unit_radius_vector
    if key_state[pygame.K_BACKSPACE]:
        velocity -= thrust * dt * unit_radius_vector

    return velocity

def handle_thrust_control(key_state, thrust_val):
    if key_state[pygame.K_UP]:
        thrust_val += 1
    if key_state[pygame.K_DOWN]:
        thrust_val -= 1
    return thrust_val

def render_objects():
    pygame.draw.circle(SCREEN, (255, 191, 0), star_pos.astype(int), 5)
    pygame.draw.circle(SCREEN, (255, 255, 255), pos.astype(int), 2)

    # Draw trail positions
    for i, trail_pos in enumerate(trail_positions):
        distance = np.linalg.norm(pos - trail_pos)
        alpha = int(255 * (1 - distance / SCREEN_WIDTH))  # Fade out trail effect based on distance
        pygame.draw.circle(SCREEN, (155, 155, 155, alpha), trail_pos.astype(int), 1)

    # Display thrust value in a box
    text_surface_thrust = font.render("Thrust: {}".format(thrust), True, (255, 255, 255))
    text_rect_thrust = text_surface_thrust.get_rect()
    text_rect_thrust.topright = (SCREEN_WIDTH - 10, 10)
    pygame.draw.rect(SCREEN, (0, 0, 0), text_rect_thrust)
    SCREEN.blit(text_surface_thrust, text_rect_thrust)

    # Display velocity magnitude below thrust value
    velocity_mag = np.linalg.norm(vel)
    text_surface_velocity = font.render("Velocity: {:.2f}".format(velocity_mag), True, (255, 255, 255))
    text_rect_velocity = text_surface_velocity.get_rect()
    text_rect_velocity.topright = (SCREEN_WIDTH - 10, 50)
    pygame.draw.rect(SCREEN, (0, 0, 0), text_rect_velocity)
    SCREEN.blit(text_surface_velocity, text_rect_velocity)

def update_trail_positions():
    trail_positions.append(pos.copy())

    # Limit the trail length
    if len(trail_positions) > trail_length:
        trail_positions.pop(0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    key_state = pygame.key.get_pressed()
    vel = handle_movement(key_state, vel)
    thrust = handle_thrust_control(key_state, thrust)

    pos, vel = add_gravitational_force(pos, vel)
    

    SCREEN.fill((0, 0, 0))
    render_objects()
    update_trail_positions()
    pygame.display.update()
    clock.tick(60)
