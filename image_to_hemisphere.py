import cv2
import numpy as np

def hemispherical_transform(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Get the dimensions of the image
    height, width, _ = image.shape

    # Define the center of the hemispherical image
    center_x = width // 2
    center_y = height

    # Create a blank hemispherical image
    hemispherical_image = np.zeros((height, width, 3), np.uint8)

    # Iterate over each pixel in the hemispherical image
    for y in range(height):
        for x in range(width):
            # Calculate the distance from the center of the hemispherical image
            distance = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)

            # Calculate the corresponding point in the original image
            original_x = int((x - center_x) * (np.sqrt(1 - (distance / width) ** 2)) + center_x)
            original_y = int(y * (np.sqrt(1 - (distance / width) ** 2)))

            # Copy the pixel from the original image to the hemispherical image
            hemispherical_image[y, x] = image[original_y, original_x]

    return hemispherical_image

# Specify the path to the input image
image_path = 'path_to_input_image.jpg'

# Transform the image into a hemispherical image
hemispherical_image = hemispherical_transform(image_path)

# Display the original and hemispherical images
cv2.imshow('Original Image', cv2.imread(image_path))
cv2.imshow('Hemispherical Image', hemispherical_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
