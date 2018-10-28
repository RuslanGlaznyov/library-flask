import os

from werkzeug.utils import secure_filename
import time as t
from config.settings import DevelopmentConfig


def create_folder(file_path):
    if not os.path.exists(file_path):
        os.mkdir(file_path)


def save_file(form_data, type_file):

    filename = secure_filename(os.path.splitext(form_data.filename)[0] + DevelopmentConfig.FILE_SPLIT
                               + str(int(t.time())) +
                               os.path.splitext(form_data.filename)[1])

    file_path = os.path.join(
        DevelopmentConfig.UPLOAD_PATH, type_file, filename
    )

    create_folder(os.path.join(DevelopmentConfig.UPLOAD_PATH, type_file))
    form_data.save(file_path)
    return file_path.split('static/')[1]
