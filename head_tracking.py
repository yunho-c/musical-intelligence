import cv2
import numpy as np
import mediapipe as mp
import pygame

# Initialize Mediapipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Eye Gaze/Head Direction Cursor")

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

        # Extract the eye or head landmarks
        # Modify these lines based on the specific landmarks you want to use for gaze or head direction
        right_eye = [face_landmarks.landmark[133], face_landmarks.landmark[173]]
        left_eye = [face_landmarks.landmark[362], face_landmarks.landmark[263]]

        # Calculate the midpoint between the eyes
        eye_center = np.mean([np.array([eye.x, eye.y]) for eye in right_eye + left_eye], axis=0)

        # Map the eye center coordinates to the screen coordinates
        cursor_x = int(eye_center[0] * screen_width)
        cursor_y = int(eye_center[1] * screen_height)

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