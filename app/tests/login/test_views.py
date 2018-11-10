from flask import url_for


class TestLogin(object):

    def test_login_page(self, client):
        response = client.get(url_for('login.login_page'))
        assert response.status_code == 200