import cv2
import mediapipe as mp
import math
import numpy as np

def initialize_mediapipe():
    mp_face_detection = mp.solutions.face_detection
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    
    face_detection = mp_face_detection.FaceDetection(
        model_selection=0,
        min_detection_confidence=0.5
    )
    
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )
    
    return face_detection, hands, mp_draw

def calculate_distance(point1, point2):
    return math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)

def get_hand_gesture(hand_landmarks):
    # Get specific landmarks
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    middle_tip = hand_landmarks.landmark[12]
    ring_tip = hand_landmarks.landmark[16]
    pinky_tip = hand_landmarks.landmark[20]
    
    # Get base points for reference
    wrist = hand_landmarks.landmark[0]
    thumb_base = hand_landmarks.landmark[2]
    index_base = hand_landmarks.landmark[5]
    middle_base = hand_landmarks.landmark[9]
    ring_base = hand_landmarks.landmark[13]
    pinky_base = hand_landmarks.landmark[17]
    
    # Calculate distances
    thumb_dist = calculate_distance(thumb_tip, thumb_base)
    index_dist = calculate_distance(index_tip, index_base)
    middle_dist = calculate_distance(middle_tip, middle_base)
    ring_dist = calculate_distance(ring_tip, ring_base)
    pinky_dist = calculate_distance(pinky_tip, pinky_base)
    
    # Threshold for considering a finger as "up"
    threshold = 0.1
    
    # Check if fingers are up
    thumb_up = thumb_dist > threshold
    index_up = index_dist > threshold
    middle_up = middle_dist > threshold
    ring_up = ring_dist > threshold
    pinky_up = pinky_dist > threshold
    
    # Recognize gestures
    if index_up and not middle_up and not ring_up and not pinky_up:
        return "Pointing"
    elif index_up and middle_up and not ring_up and not pinky_up:
        return "Victory"
    elif index_up and middle_up and ring_up and pinky_up and not thumb_up:
        return "Four"
    elif index_up and middle_up and ring_up and pinky_up and thumb_up:
        return "High Five"
    elif not index_up and not middle_up and not ring_up and not pinky_up and thumb_up:
        return "Thumbs Up"
    elif not index_up and not middle_up and not ring_up and not pinky_up and not thumb_up:
        return "Fist"
    elif pinky_up and not index_up and not middle_up and not ring_up:
        return "Rock On"
    else:
        return "Unknown"

def main():
    cap = cv2.VideoCapture(0)
    
    # Set camera resolution to maximum
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Full HD width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # Full HD height
    
    face_detection, hands, mp_draw = initialize_mediapipe()
    
    # Create a named window and set it to fullscreen
    window_name = 'Face and Hand Gesture Detection'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Failed to capture frame")
            continue
        
        # Get screen dimensions
        screen_height, screen_width = image.shape[:2]
        
        # Flip the image horizontally
        image = cv2.flip(image, 1)
        
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process face detection
        face_results = face_detection.process(image_rgb)
        
        # Process hand detection
        hand_results = hands.process(image_rgb)
        
        # Draw face detections with larger visualization
        if face_results.detections:
            for detection in face_results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = image.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                       int(bboxC.width * iw), int(bboxC.height * ih)
                
                # Thicker rectangle for better visibility
                cv2.rectangle(image, bbox, (0, 255, 0), 3)
                confidence = detection.score[0]
                
                # Larger text for face confidence
                cv2.putText(image, f'Face: {int(confidence * 100)}%', 
                           (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 
                           1.2, (0, 255, 0), 3)
        
        # Draw hand landmarks and detect gestures
        if hand_results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(hand_results.multi_hand_landmarks):
                # Draw landmarks with thicker lines
                mp_draw.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp.solutions.hands.HAND_CONNECTIONS,
                    mp_draw.DrawingSpec(color=(0, 0, 255), thickness=3, circle_radius=4),
                    mp_draw.DrawingSpec(color=(0, 255, 0), thickness=3)
                )
                
                # Get and display hand gesture
                gesture = get_hand_gesture(hand_landmarks)
                
                # Calculate position for text
                h, w, _ = image.shape
                x = int(min([lm.x for lm in hand_landmarks.landmark]) * w)
                y = int(min([lm.y for lm in hand_landmarks.landmark]) * h)
                
                # Larger text for gesture
                cv2.putText(image, f'Gesture: {gesture}', 
                           (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 
                           1.5, (255, 0, 0), 3)
        
        # Display FPS with larger text
        fps = cap.get(cv2.CAP_PROP_FPS)
        cv2.putText(image, f'FPS: {int(fps)}', (20, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        
        # Add instructions
        cv2.putText(image, "Press 'Q' to quit, 'F' to toggle fullscreen", 
                    (20, screen_height - 40), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (255, 255, 255), 2)
        
        # Show the image
        cv2.imshow(window_name, image)
        
        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('f'):
            # Toggle fullscreen
            fullscreen = cv2.getWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                                cv2.WINDOW_NORMAL if fullscreen == cv2.WINDOW_FULLSCREEN else cv2.WINDOW_FULLSCREEN)
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
