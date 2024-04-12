import cv2
import numpy as np
import mediapipe as mp

class HeadTracker:
    def __init__(self):
        # Initialize MediaPipe
        mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
        self.cap = None;

        # Assuming no lens distortion
        self.dist_coeffs = np.zeros((4, 1))

    def start(self):
        # Capture video from the default camera (index 0)
        self.cap = cv2.VideoCapture(0)
        
        success, image = self.cap.read()
        # Camera matrix (assuming a generic camera)
        focal_length = image.shape[1]
        center = (image.shape[1] / 2, image.shape[0] / 2)
        self.camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype=np.float64)


    def estimate_pose(self, image, face_landmarks):
        # Landmark indices for points 1, 33, 263, 61, 291, and 199
        landmark_indices = [1, 33, 263, 61, 291, 199]

        # 3D model points (assuming a generic face model)
        model_points = np.array([
            (0.0, 0.0, 0.0),       # Nose tip
            (-225.0, 170.0, -135.0),  # Left eye left corner
            (225.0, 170.0, -135.0),   # Right eye right corner
            (-150.0, -150.0, -125.0),  # Mouth left corner
            (150.0, -150.0, -125.0),   # Mouth right corner
            (0.0, -330.0, -65.0)      # Chin
        ], dtype=np.float64)

        # Extract the landmark coordinates
        landmarks = np.array([(lm.x * image.shape[1], lm.y * image.shape[0]) for lm in face_landmarks.landmark])[landmark_indices]

        # Estimate the pose using solvePnP
        success, rotation_vector, translation_vector = cv2.solvePnP(model_points, landmarks, self.camera_matrix, self.dist_coeffs)

        return success, rotation_vector, translation_vector
        # return success, rotation_vector, translation_vector, camera_matrix, dist_coeffs

    # while self.cap.isOpened():
    def step(self):
        success, image = self.cap.read()
        if not success:
            return -1
        rotation_vector = None

        # Convert the BGR image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image and detect the face landmarks
        results = self.face_mesh.process(image_rgb)

        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]

            # Estimate the pose
            success, rotation_vector, translation_vector = self.estimate_pose(image, face_landmarks)
            # success, rotation_vector, translation_vector, camera_matrix, dist_coeffs = self.estimate_pose(image, face_landmarks)

            if success:
                # Draw the axes representing the rotation and translation vectors
                axes_length = 100
                cv2.drawFrameAxes(image, self.camera_matrix, self.dist_coeffs, rotation_vector, translation_vector, axes_length)

        # Display the image
        cv2.imshow('Face Pose Estimation', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return -1
        
        if rotation_vector is not None: 
            # return rotation_vector
            rotmat, jacobian = cv2.Rodrigues(rotation_vector)
            return rotmat @ np.array([0.0, 0.0, 1.0])


    def end(self):
        self.cap.release()
        cv2.destroyAllWindows()