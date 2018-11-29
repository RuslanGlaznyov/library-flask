import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from app.blueprints.library.models import Genre
import time as t
import lib.util_file_form_storage as st

from werkzeug.utils import secure_filename

from config.settings import DevelopmentConfig


def auth():
    gauth = GoogleAuth()

    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
        gauth.SaveCredentialsFile("mycreds.txt")

    drive = GoogleDrive(gauth)

    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

    main_folder_id = 0
    for file in file_list:
        if file['title'] == 'library':
            main_folder_id = file['id']

    return drive, main_folder_id


def is_folder_exist(title, drive, main_folder_id):
    folder_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(main_folder_id)}).GetList()
    if title in [folder['title'] for folder in folder_list]:
        return True

    return False


def create_folder(genre_name, drive, main_folder_id):
    genre = Genre.query.filter_by(title=genre_name).first()
    if not is_folder_exist(genre_name, drive, main_folder_id):
        folder = drive.CreateFile({'title': genre_name, 'parents': [{'id': main_folder_id}],
                                   'mimeType': 'application/vnd.google-apps.folder'})
        folder.Upload()
        genre.folder_google_id = folder['id']
        genre.save()
    return genre


def save_file(form_data, type_file):
    drive, main_folder_id = auth()

    genre = create_folder(type_file, drive, main_folder_id)
    path_to_file = st.save_file(form_data, 'temp')

    filename = path_to_file.split('/')[-1]

    file_to_disc = drive.CreateFile({'title': filename, 'parents': [{'id': genre.folder_google_id}]})

    file_to_disc.SetContentFile('app/static/' + path_to_file)
    file_to_disc.Upload()

    file_id = file_to_disc['id']
    st.clear_dir(DevelopmentConfig.BASEDIR + '/app/static/uploads/temp')
    return file_id

