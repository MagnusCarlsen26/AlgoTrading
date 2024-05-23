import os
import pandas as pd
import shutil  # Import shutil for rmtree

def process_folders_in_directory(directory):
    folders_to_delete = []

    for folder in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, folder)) and not folder.startswith('.'):
            folder_path = os.path.join(directory, folder)
            csv_path = os.path.join(folder_path, 'yes.csv')

            try:
                df = pd.read_csv(csv_path)
                if len(df) < 2600:
                    folders_to_delete.append(folder_path)
            except FileNotFoundError:
                print(f"Warning: 'yes.csv' not found in {folder}")

    return folders_to_delete

if __name__ == "__main__":
    folders_to_delete = process_folders_in_directory('.')

    if folders_to_delete:
        print("\nDeleting folders:")
        for folder in folders_to_delete:
            try:
                shutil.rmtree(folder)  # Use shutil.rmtree() to delete non-empty folders
                print(f"Deleted: {folder}")
            except OSError as e:
                print(f"Error deleting {folder}: {e}")
    else:
        print("No folders found with less than 2500 entries in 'yes.csv'.")
