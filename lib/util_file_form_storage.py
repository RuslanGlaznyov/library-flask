import os
import shutil

from werkzeug.utils import secure_filename
import time as t
from config.settings import DevelopmentConfig


def create_folder(file_path):
    upload_dir = os.path.join(DevelopmentConfig.BASEDIR, DevelopmentConfig.UPLOAD_PATH)
    if not os.path.exists(upload_dir):
        os.mkdir(upload_dir)

    if not os.path.exists(file_path):
        os.mkdir(file_path)


def save_file(form_data, type_file, custom_name=None, fake_file=False):
    if fake_file:
        filename, ext = os.path.splitext(os.path.basename(form_data))
    else:
        filename, ext = os.path.splitext(form_data.filename)

    if custom_name:
        filename = custom_name

    unique_filename = secure_filename(filename + DevelopmentConfig.FILE_SPLIT
                                      + str(int(t.time())) + ext)

    file_path = os.path.join(
        DevelopmentConfig.BASEDIR,
        DevelopmentConfig.UPLOAD_PATH, type_file, unique_filename
    )

    create_folder(os.path.join(DevelopmentConfig.BASEDIR, DevelopmentConfig.UPLOAD_PATH, type_file))
    if fake_file:
        shutil.copy2(form_data, file_path)
    else:
        form_data.save(file_path)

    return file_path.split('static/')[1]


def delete_file(file_path):
    path = os.path.join(DevelopmentConfig.DOWNLOAD_PATH, file_path)
    if os.path.exists(path):
        os.remove(os.path.abspath(path))

    array_path = path.split('/')[0:-1]
    path_remove = '/'.join(array_path)
    try:
        if not os.listdir(path_remove):
            os.rmdir(path_remove)
    except Exception as e:
        pass

