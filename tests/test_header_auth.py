import json
from ._header_base import HeaderCase


class TestHeaderAuth(HeaderCase):
    def test_unlogin_index(self):
        response = self.client.open("/")
        assert response._status_code == 401

    def test_login_index(self):
        response = self.client.post("/login", data=dict(
            name='foo'
        ))
        data = json.loads(response.data)
        response = self.client.get(
            '/',
            headers={'Authorization': 'Bearer %s' % data['token']})
        assert response._status_code == 200

    def test_permission(self):
        response = self.client.post("/login", data=dict(
            name='foo'
        ))
        data = json.loads(response.data)
        response = self.client.get(
            '/edit',
            headers={'Authorization': 'Bearer %s' % data['token']})
        assert response._status_code == 200
