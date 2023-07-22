import os
import time

def rename_images(folder_path):
    files = os.listdir(folder_path)
    
    for file in files:
        if file.lower().endswith('.jpg'):
            file_name, file_ext = os.path.splitext(file)
            new_file_name = file_name + '_4.jpg'
            old_file_path = os.path.join(folder_path, file)
            new_file_path = os.path.join(folder_path, new_file_name)
            os.rename(old_file_path, new_file_path)
            print(f"Renamed {file} to {new_file_name}")

start = time.time()
folder_path = 'images/v1/patch0/'
rename_images(folder_path)
end = time.time()

time_taken = (end - start)/60
print(time_taken)