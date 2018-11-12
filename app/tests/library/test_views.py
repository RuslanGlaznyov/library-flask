from flask import url_for
from app.blueprints.library.models import Book, Note


class TestPage(object):
    def test_index_page(self, client):
        response = client.get(url_for('library.index'))
        assert response.status_code == 200

    def test_new_form_page(self, client):
        form = {
            'title': 'test',
            'desc': 'Test description',
            'new_genre': 'test genre',
        }

        response = client.post(url_for('library.new'), data=form,
                               follow_redirects=True)
        assert response.status_code == 200
        # assert_status_with_message(200, response, 'Thanks')

    def test_detail_page(self, client):
        response = client.get(url_for('library.detail', genre='test', book_id=1, title='test'))
        assert response.status_code == 200

    def test_new_note(self, client):
        params = {
            'text': 'test'
        }
        response = client.post(url_for('library.detail', genre='test', book_id=1, title='test'), data=params,
                               follow_redirects=True)

        assert response.status_code == 200

    def test_edit_note(self, client):
        params = {
            'text': 'edit test'
        }

        response = client.post(url_for('library.edit_note', genre='test', book_id=1, title='test', note_id=1),
                               data=params
                               )
        assert response.status_code == 200
        assert b'edit test' in response.data

    def test_set_rating(self, client):
        response = client.post(url_for('library.set_rating', genre='test', book_id=1, title='test', rating=1),
                               follow_redirects=True)
        assert response.status_code == 200
        assert Book.query.get(1).rating == 1

    def test_change_status(self, client):
        response = client.post(url_for('library.change_status', genre='test', book_id=1, title='test', status='Done'),
                               follow_redirects=True)

        assert response.status_code == 200
        assert Book.query.get(1).status == 'Done'

    def test_delete_note(self, client):
        response = client.post(url_for('library.delete_note', genre='test', book_id=1, title='test', note_id=1),
                               follow_redirects=True)

        assert response.status_code == 200
        assert Note.query.get(1) is None

    def test_download_book(self, client):
        response = client.get(url_for('library.download_book', genre='test', book_id=1, title='test'),
                              follow_redirects=True)

        assert response.status_code == 500


