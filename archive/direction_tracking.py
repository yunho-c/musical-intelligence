import cv2
import numpy as np
import mediapipe as mp
import pygame
import math

# Initialize Mediapipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Face Direction Cursor")

# Main loop
cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Flip the image horizontally for a later selfie-view display
    image = cv2.flip(image, 1)

    # Convert the BGR image to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and detect the face landmarks
    results = face_mesh.process(image)

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]

        # Get the screen dimensions
        screen_width, screen_height = screen.get_size()

        # Extract the nose and chin landmarks
        nose_landmark = face_landmarks.landmark[1]
        chin_landmark = face_landmarks.landmark[175]

        # Calculate the direction vector of the face
        direction_vector = np.array([chin_landmark.x - nose_landmark.x, chin_landmark.y - nose_landmark.y])
        direction_vector = direction_vector / np.linalg.norm(direction_vector)

        # Calculate the angle of the face direction vector
        angle = math.atan2(direction_vector[1], direction_vector[0])

        # Map the angle to the screen coordinates
        cursor_x = int((angle + math.pi) / (2 * math.pi) * screen_width)
        cursor_y = int(screen_height / 2)

        # Clear the Pygame screen
        screen.fill((255, 255, 255))

        # Draw the cursor on the Pygame screen
        pygame.draw.circle(screen, (255, 0, 0), (cursor_x, cursor_y), 10)

        # Update the Pygame display
        pygame.display.update()

    # Check for Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            exit()

# Release the video capture and quit Pygame
cap.release()
pygame.quit()