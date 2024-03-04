import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=4, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Function to calculate the angle between two vectors in degrees, range [0, 360).
# The angle is adjusted to increase counterclockwise.
def calculate_counterclockwise_angle(v1, v2):
    angle = np.arctan2(v2[0], -v2[1]) - np.arctan2(v1[0], -v1[1])
    if angle < 0:
        angle += 2 * np.pi
    return np.degrees(angle)

# Start capturing video from the webcam.
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Flip the frame horizontally for a correct selfie-view display.
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw the hand landmarks.
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Retrieve the required landmarks.
            mcp_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
            tip_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            
            # Inverted vertical vector to align with the traditional y-axis direction.
            vertical_vector = np.array([0, 1])
            
            # Vector from MCP to fingertip.
            finger_vector = np.array([tip_landmark.x - mcp_landmark.x, -(tip_landmark.y - mcp_landmark.y)])  # Note the negation of the y-component
            
            # Calculate the angle between the two vectors.
            angle = calculate_counterclockwise_angle(vertical_vector, finger_vector)
            
            # Normalize the angle to be between 0 and 360
            angle = angle % 360
            
            # Display the angle on the frame.
            cv2.putText(frame, f'Angle: {angle:.2f} degrees', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Show the flipped frame.
    cv2.imshow('MediaPipe Hands', frame)

    # Exit loop when pressing 'ESC'.
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Release resources.
hands.close()
cap.release()
cv2.destroyAllWindows()
