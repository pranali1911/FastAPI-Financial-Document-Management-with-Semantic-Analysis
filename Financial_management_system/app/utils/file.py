# This will handle file saving and retrieval
import shutil

def save_file(file, filename):
    file_path = f"uploads/{filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file, buffer)

    return file_path