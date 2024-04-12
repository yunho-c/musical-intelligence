import pygame
import numpy as np
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D First-Person Environment")

# Set up colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Set up the camera
camera_pos = np.array([0, 0, 0], dtype=np.float32)
camera_yaw = 0
camera_pitch = 0

camera_speed = 0.01

# Set up the environment
wall_coordinates = [
    [np.array([-1, -1, 1], dtype=np.float32), np.array([1, -1, 1], dtype=np.float32)],
    [np.array([1, -1, 1], dtype=np.float32), np.array([1, 1, 1], dtype=np.float32)],
    [np.array([1, 1, 1], dtype=np.float32), np.array([-1, 1, 1], dtype=np.float32)],
    [np.array([-1, 1, 1], dtype=np.float32), np.array([-1, -1, 1], dtype=np.float32)]
]

# Set up the projection parameters
fov = 90
near_plane = 0.1
far_plane = 100

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.MOUSEMOTION:
        #     mouse_movement = event.rel
        #     camera_yaw += mouse_movement[0] * 0.1
        #     camera_pitch += mouse_movement[1] * 0.1

    # Handle keyboard input for camera movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera_pitch -= camera_speed
    if keys[pygame.K_s]:
        camera_pitch += camera_speed
    if keys[pygame.K_a]:
        camera_yaw += camera_speed
    if keys[pygame.K_d]:
        camera_yaw -= camera_speed

    # Clear the display
    display.fill(BLACK)

    # Calculate the camera's orientation
    camera_rot_x = np.array([[1, 0, 0],
                            [0, math.cos(math.radians(camera_pitch)), -math.sin(math.radians(camera_pitch))],
                            [0, math.sin(math.radians(camera_pitch)), math.cos(math.radians(camera_pitch))]])
    camera_rot_y = np.array([[math.cos(math.radians(camera_yaw)), 0, math.sin(math.radians(camera_yaw))],
                            [0, 1, 0],
                            [-math.sin(math.radians(camera_yaw)), 0, math.cos(math.radians(camera_yaw))]])
    camera_rot = np.dot(camera_rot_y, camera_rot_x)

    # Calculate the view matrix
    view_matrix = np.eye(4)
    view_matrix[:3, :3] = camera_rot
    view_matrix[:3, 3] = -np.dot(camera_rot, camera_pos)

    # Draw the walls
    for wall in wall_coordinates:
        projected_points = []
        for point in wall:
            # Transform the 3D point to camera space
            point_camera = np.dot(view_matrix, np.append(point, 1))[:3]
            
            # Project the point onto the 2D screen
            if point_camera[2] != 0:
                px = (point_camera[0] / point_camera[2]) * (width / 2) + (width / 2)
                py = (point_camera[1] / point_camera[2]) * (height / 2) + (height / 2)
                projected_points.append((px, py))
        
        if len(projected_points) == 2:
            pygame.draw.line(display, WHITE, projected_points[0], projected_points[1], 2)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()