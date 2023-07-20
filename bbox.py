#shows the bbox of images in a folder given the class labels in a file classes.txt, images in images folder
#and labels in labels folder. It saves the images with the bboxes in another folder names output_images
import cv2
import os

def parse_yolov7_label(label_path, image_width, image_height, class_names):
    with open(label_path, 'r') as file:
        lines = file.readlines()

    boxes = []
    for line in lines:
        data = line.strip().split()
        class_index = int(data[0])
        x_center = float(data[1]) * image_width
        y_center = float(data[2]) * image_height
        box_width = float(data[3]) * image_width
        box_height = float(data[4]) * image_height

        x_min = int(x_center - box_width / 2)
        y_min = int(y_center - box_height / 2)
        x_max = int(x_center + box_width / 2)
        y_max = int(y_center + box_height / 2)

        boxes.append((x_min, y_min, x_max, y_max, class_index))

    return boxes

def draw_boxes_on_image(image_path, boxes, class_names):
    image = cv2.imread(image_path)
    for box in boxes:
        x_min, y_min, x_max, y_max, class_index = box
        class_name = class_names[class_index]

        color = (0, 255, 0)  # Green color for bounding boxes
        thickness = 2
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, thickness)

        # Display class name alongside the bounding box
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        text = f"{class_name}"
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = x_min
        text_y = y_min - 5 if y_min - 5 > 0 else y_min + 15
        cv2.rectangle(image, (text_x, text_y - text_size[1]), (text_x + text_size[0], text_y), color, -1)
        cv2.putText(image, text, (text_x, text_y), font, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)


def save_image_with_boxes(image_path, output_folder, boxes, class_names):
    image = cv2.imread(image_path)
    image_height, image_width, _ = image.shape

    for box in boxes:
        x_min, y_min, x_max, y_max, class_index = box
        class_name = class_names[class_index]

        color = (0, 255, 0)  # Green color for bounding boxes
        thickness = 2
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, thickness)

        # Display class name alongside the bounding box
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        text = f"{class_name}"
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = x_min
        text_y = y_min - 5 if y_min - 5 > 0 else y_min + 15
        cv2.rectangle(image, (text_x, text_y - text_size[1]), (text_x + text_size[0], text_y), color, -1)
        cv2.putText(image, text, (text_x, text_y), font, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)

    output_image_path = os.path.join(output_folder, os.path.basename(image_path))
    cv2.imwrite(output_image_path, image)


images_folder = 'images'
labels_folder = 'labels'
classes_file = 'classes.txt'
output_folder = 'output_images'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Read class names from the classes file
with open(classes_file, 'r') as file:
    class_names = [line.strip() for line in file.readlines()]

image_files = os.listdir(images_folder)
for image_file in image_files:
    image_path = os.path.join(images_folder, image_file)
    label_path = os.path.join(labels_folder, image_file.replace('.jpg', '.txt'))

    if os.path.exists(label_path):
        image = cv2.imread(image_path)
        image_height, image_width, _ = image.shape

        boxes = parse_yolov7_label(label_path, image_width, image_height, class_names)
        draw_boxes_on_image(image_path, boxes, class_names)
        save_image_with_boxes(image_path, output_folder, boxes, class_names)
    else:
        print(f"Label not found for {image_file}")
