import os
from flask import url_for, current_app
from PIL import Image

def add_profile_picture(username, uploaded_picture):
    extension = uploaded_picture.filename.split(".")[-1]

    filename = str(username) + "." + extension

    path = os.path.join(current_app.root_path, "static/profile_pictures", filename)

    picture = Image.open(uploaded_picture)

    size = (200, 200)

    picture.thumbnail(size)
    picture.save(path)

    return filename
