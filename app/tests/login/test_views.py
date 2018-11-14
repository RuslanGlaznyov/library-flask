from flask import url_for
from config.settings import DevelopmentConfig
from lib.test import ViewTestMixin


class TestLogin(ViewTestMixin):
    def test_login_page(self, client):
        response = client.get(url_for('login.login_page'))
        assert response.status_code == 200

    def test_login(self, client):
        response = self.login()
        with client.session_transaction() as session:
            assert session['password'] == DevelopmentConfig.PASSWORD

    def test_logout(self, client):
        response = self.logout()
        assert response.status_code == 200