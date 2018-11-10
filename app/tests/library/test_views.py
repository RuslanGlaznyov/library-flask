from flask import url_for


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
