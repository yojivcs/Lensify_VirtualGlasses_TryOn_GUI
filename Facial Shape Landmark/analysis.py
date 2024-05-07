import cv2
import math

# Define the facial landmark points
LANDMARK_POINTS = [
    (30, 30), (36, 30), (42, 30), (48, 30), (54, 30), (60, 30), (66, 30),
    (33, 36), (39, 36), (45, 36), (51, 36), (57, 36), (63, 36),
    (36, 42), (42, 42), (48, 42), (54, 42), (60, 42), (66, 42),
    (42, 48), (48, 48), (54, 48), (60, 48),
    (48, 54), (54, 54), (60, 54),
    (54, 60), (60, 60),
    (60, 66),
]

# Define the facial shape categories
FACIAL_SHAPES = {
    'oval': (1.3, 1.5),  # length to width ratio
    'round': (1.0, 1.2),
    'oblong': (1.5, 1.7),
    'square': (0.9, 1.1),
    'triangle': (1.2, 1.4),
    'diamond': (1.4, 1.6),
    'heart': (1.1, 1.3)
}

def calculate_facial_shape(landmarks):
    # Calculate the facial dimensions
    width = math.hypot(landmarks[0][0] - landmarks[-1][0], landmarks[0][1] - landmarks[-1][1])
    length = math.hypot(landmarks[8][0] - landmarks[26][0], landmarks[8][1] - landmarks[26][1])
    ratio = length / width

    # Determine the facial shape
    for shape, (min_ratio, max_ratio) in FACIAL_SHAPES.items():
        if min_ratio <= ratio <= max_ratio:
            return shape

    return 'unknown'

def detect_landmarks(image_path):
    # Read the image
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect the facial landmark points
    landmarks = [(point[0], point[1]) for point in LANDMARK_POINTS]
    for point in landmarks:
        cv2.circle(image, point, 3, (0, 0, 255), -1)
    
    return landmarks

def analyze_image(image_path):
    # Detect the facial landmarks
    landmarks = detect_landmarks(image_path)
    
    # Calculate the facial shape
    facial_shape = calculate_facial_shape(landmarks)
    
    print(f'Facial Shape: {facial_shape}')

# Call the analyze_image function with the image file path
image_path = (r'E:\MyProjects\Lensify Try on Your Vision, Virtually\Source Code\Basic Virtual Try On - TestI\virtual_glasses_try_on_test_code\Facial Landmarks\captured_images\Tahasin.jpg')
analyze_image(image_path)