import cv2

def process_image(image, operation):
    # Load the image
    # img = cv2.imread(image, cv2.IMREAD_COLOR)
    # Perform the specified operation
    if operation == 'edge_detection':
        result = cv2.Canny(image, 100, 200)
    elif operation == 'color_inversion':
        result = cv2.bitwise_not(image)
    # Add more operations as needed...
    return result