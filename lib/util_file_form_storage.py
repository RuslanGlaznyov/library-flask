import os

from werkzeug.utils import secure_filename
import time as t
from config.settings import DevelopmentConfig


def create_folder(file_path):
    if not os.path.exists(file_path):
        os.mkdir(file_path)


def save_file(form_data, type_file, custom_name=None):
    filename, ext = os.path.splitext(form_data.filename)
    if custom_name:
        filename = custom_name

    unique_filename = secure_filename(filename + DevelopmentConfig.FILE_SPLIT
                                      + str(int(t.time())) + ext)

    file_path = os.path.join(
        DevelopmentConfig.UPLOAD_PATH, type_file, unique_filename
    )

    create_folder(os.path.join(DevelopmentConfig.UPLOAD_PATH, type_file))
    form_data.save(file_path)
    return file_path.split('static/')[1]


def get_file(file_path):
    f, ext = os.path.splitext(file_path)
    standard_name = file_path.split('/')[-1].split(DevelopmentConfig.FILE_SPLIT)[0] + ext
    array_path = file_path.split('/')
    array_path[-1] = standard_name
    return '/'.join(array_path)


def delete_file(file_path):
    os.remove(os.path.abspath('app/static/' + file_path))

