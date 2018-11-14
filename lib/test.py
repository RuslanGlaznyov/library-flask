import pytest
from flask import url_for, session
from config.settings import DevelopmentConfig
from app.run_app import flask_app


class ViewTestMixin(object):

    @pytest.fixture(autouse=True)
    def set_common_fixtures(self, client):
        # self.session = session
        self.client = client

    def login(self, password=DevelopmentConfig.PASSWORD):
        with self.client.session_transaction() as session:
            session['password'] = password

        return login(self.client, password)

    def logout(self):
        return logout(self.client)


def login(client, password=''):
    user = dict(password=password)
    response = client.post(url_for('login.login_page'), data=user,
                           follow_redirects=True)

    return response


def logout(client):
    return client.get(url_for('login.log_out'), follow_redirects=True)
