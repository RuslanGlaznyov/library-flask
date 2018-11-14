from flask import url_for

from lib.test import ViewTestMixin


class TestStat(ViewTestMixin):
    def test_index_page(self, client):
        self.login()
        response = client.get(url_for('stat.index'))
        assert response.status_code == 200
