from flask import url_for


class TestStat(object):
    def test_index_page(self, client):
        response = client.get(url_for('stat.index'))
        assert response.status_code == 200
