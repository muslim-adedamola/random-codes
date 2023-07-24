import os

def rename_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith("_4_4.jpg"):
            new_filename = filename[:-8] + ".jpg"
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, new_filename)
            os.rename(old_file_path, new_file_path)


folder_path = "path/to/your/folder"  # Replace this with the path to your folder containing images
rename_files(folder_path)
