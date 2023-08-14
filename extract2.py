import json
import os
import time

input_path = "images/v1/patch0"

with open('zhiyuan_objv2_train.json') as f:
    data = json.load(f)

# Make a list of annotations of images present in a patch
def get_image_annotation(image_id):
    image_ann = []
    for ann in data['annotations']:
        if ann['image_id'] == image_id:
            image_ann.append(ann)
    return image_ann

# Returns the corresponding image dictionary of a particular image filename
def get_image(filename):
    for img in data['images']:
        if img['file_name'] == filename:
            return img

file_names = []

# Loads images from a folder
def load_images_from_folder(folder):
    for filename in os.listdir(folder):
        filename = os.path.join(input_path, filename)
        file_names.append(filename)
        print(filename)

load_images_from_folder(input_path)

start = time.time()

with open("classes.txt", "w") as file_with_annotations:
    count = 0
    for filename in file_names:
        img = get_image(filename)
        img_id = img['id']
        img_ann = get_image_annotation(img_id)

        if img_ann:
            for ann in img_ann:
                current_category = ann['category_id']
                file_with_annotations.write(f"{current_category}\n")
                print(f"{current_category}\t{filename}")
        count += 1

end = time.time()
time_needed = (end - start) / 60
print(time_needed)